# Everpure OpenStack: initiator identity audit and remediation

Compute nodes built from a gold image that already contains
`/etc/iscsi/initiatorname.iscsi` or `/etc/nvme/hostnqn` all present the same
IQN or NQN to the FlashArray. The Cinder driver looks host objects up by
initiator identity, so every node collapses onto one host object: volumes
attached on one node become visible on another, detaches on one node remove
connections another is using, and multipath sees paths come and go across the
fleet. It is one of the most common root causes in OpenStack support cases and
is treated at data-integrity severity (escalation runbook, section 6.1).

These playbooks detect it, fix it safely, and clean up the array afterwards.

| Playbook | What it does | Changes anything? |
|---|---|---|
| `01_audit_initiator_identity.yml` | Collects IQN, NQN, NVMe host ID and machine-id from every compute node, reports duplicates, nodes with no identity and nodes that could not be reached, writes a JSON report, exits non-zero on duplicates (pipeline gate) | No |
| `02_remediate_initiator_identity.yml` | Regenerates identities on the targeted nodes, **one node at a time**, with gates: explicit confirmation, no running instances, no active storage sessions; backs up old files; restarts iscsid and nova-compute; verifies the new values differ from the old | Yes, on hosts |
| `03_flasharray_cleanup_stale_hosts.yml` | Finds FlashArray host objects keyed on the duplicate identities; deletes only those with **no** connected volumes (re-checked immediately before the delete, and not in a host group unless allowed); reports the rest for manual reconciliation | Yes, on the array, only with confirmation |

## Requirements

* Ansible core 2.16 or later on the controller (required by the collection).
* `everpure.flasharray` collection for playbook 03
  (`ansible-galaxy collection install everpure.flasharray`). The older
  `purestorage.flasharray` name is now a redirect shim and will be removed.
* `iscsi-initiator-utils`/`open-iscsi` and `nvme-cli` on the compute nodes.
* A FlashArray API token with permission to delete hosts (playbook 03). Put it
  in the `PUREFA_API` environment variable rather than on the command line.

## Workflow

```bash
# 1. Audit. Read-only. Fails if duplicates exist.
ansible-playbook -i inventory playbooks/01_audit_initiator_identity.yml

# 2. Evacuate the flagged nodes (live-migrate instances off them), then remediate
#    one node at a time. Limit to the nodes the report named.
ansible-playbook -i inventory playbooks/02_remediate_initiator_identity.yml \
    -l compute-03,compute-07 -e confirm_remediation=true

# 3. Re-audit to confirm uniqueness.
ansible-playbook -i inventory playbooks/01_audit_initiator_identity.yml

# 4. Clean up the shared host object(s) on each FlashArray behind the backend.
#    Dry run first, then with confirmation.
export PUREFA_API=<token>
ansible-playbook playbooks/03_flasharray_cleanup_stale_hosts.yml \
    -e fa_url=array01.example.com \
    -e audit_report=reports/initiator_identity_<timestamp>.json
ansible-playbook playbooks/03_flasharray_cleanup_stale_hosts.yml \
    -e fa_url=array01.example.com \
    -e audit_report=reports/initiator_identity_<timestamp>.json -e confirm_cleanup=true

# 5. Verify per runbook 6.1: attach a test volume on two nodes and confirm two
#    distinct host objects, one connection each.
```

Use the audit report from step 1 (before remediation) for step 4: it holds the
*old* duplicate values that the stale host objects are keyed on.

Do not run the audit with `-l`: its second play runs on localhost, which a
host limit excludes, so no analysis or report would be produced. Target a
different set of nodes with `-e compute_group=<group>` instead. The audit exits
2 on duplicates and 4 when any node was unreachable, so either is non-zero for
a pipeline gate; unreachable nodes are listed under `not_collected` in the
report and only fail the run with `-e fail_on_unreachable=true`.

## Distribution notes

`02_remediate` needs to know how to restart nova-compute and iscsid. Set
`openstack_distribution` in group_vars or with `-e`
(see `group_vars/compute.yml.example`):

| Value | nova-compute restart | iscsid restart |
|---|---|---|
| `rhoso` | `systemctl restart edpm_nova_compute.service` (EDPM data-plane node) | `systemctl restart edpm_iscsid.service` |
| `rhosp` | `systemctl restart tripleo_nova_compute.service` | `systemctl restart tripleo_iscsid.service` |
| `charmed` | `systemctl restart nova-compute.service` | `systemctl restart iscsid.service` |
| `kolla` | `podman`/`docker restart nova_compute` | `podman`/`docker restart iscsid` |
| `package` | `systemctl restart nova-compute.service` | `systemctl restart iscsid.service` |

On RHOSP, RHOSO and Kolla, iscsid runs inside a container with `/etc/iscsi`
bind-mounted from the host. The container holds the cached initiator name, so
it is the container that must be restarted; a host `iscsid.service` restart
would not be enough. Confirm the unit or container names on your deployment
before running; override `nova_restart_commands` and `iscsid_restart_commands`
if they differ (entries are merged over the defaults).

## Prevention

Stop the problem at the source:

* `files/gold-image-cleanup.sh`: run as the last step before sealing a gold
  image. Removes the identity files and empties `/etc/machine-id`.
* `files/cloud-init-initiator-identity.yaml`: first-boot generation of IQN, NQN
  and host ID, for deployments that use cloud-init. Deployment tools with their
  own first-boot hooks (TripleO/EDPM, Juju, Kolla) should do the equivalent.
* Add `01_audit_initiator_identity.yml` to deployment validation and to the
  quarterly top-25 health review; its non-zero exit on duplicates makes it a
  pipeline gate.

Why NVMe needs the first-boot step even where iSCSI does not: iscsid
regenerates a missing initiator name at boot on both RHEL and Ubuntu, but
nothing ever regenerates `/etc/nvme/hostnqn`. The `nvme-cli` package creates it
once at install time, which is exactly how it ends up baked into a gold image.

`nvme gen-hostnqn` derives the NQN from the DMI product UUID. Servers that ship
with an identical or placeholder product UUID would regenerate the very same
duplicate, so both the cloud-init step and playbook 02 fall back to a random
UUID when the generated value is unusable or equals the value being replaced,
and write the same UUID to `/etc/nvme/hostid`.

## Safety

* Playbook 02 refuses to run without `-e confirm_remediation=true`, refuses a
  node with running instances (or whose libvirt cannot be queried) unless
  `-e allow_running_instances=true`, and refuses a node with active iSCSI
  sessions or NVMe-oF controllers unless `-e allow_active_sessions=true`. Local
  PCIe NVMe drives are not counted. It runs `serial: 1`, stops at the first
  failure, and verifies on each node that the new identities are present and
  differ from the old ones before moving to the next. Old identity files are
  backed up under `/root/initiator-identity-backup/`.
* Playbook 03 is a dry run by default and never deletes a host object that
  still has volumes connected. The connection count is re-read immediately
  before each delete. Objects with connections are listed for manual
  reconciliation against `openstack volume attachment list`, as the runbook
  requires. Be aware that `purefa_host state=absent` would itself disconnect
  volumes before deleting, which is why the guard in the playbook matters.
* Playbook 03 reads host objects from the `hosts` subset of `purefa_info`
  (`hosts.<name>.iqn`, `.nqn`, `.hgroup`, `.volumes`), verified against
  everpure.flasharray 1.44/1.45. Host objects scoped to a realm are out of
  scope and ignored.

## Status

Draft v0.2, October 2026. Intended for inclusion in the Everpure Ansible
collections once reviewed. Owner: Simon Dodsley.
