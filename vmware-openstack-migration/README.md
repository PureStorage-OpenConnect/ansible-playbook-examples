# VMware to OpenStack VM Migration

This repository contains Ansible playbooks designed to automate the migration of virtual machines (VMs) from a VMware vSphere platform to an OpenStack environment. The process leverages VMware vVols and the volume group handling capabilities provided by the Pure Storage Cinder driver.

---

## 🧭 Migration Workflow Overview

This utility is implemented as a single Ansible role composed of modular tasks executed sequentially as a complete workflow.

The workflow assumes:
- Source VMs are stored on a VMFS datastore.
- Each VM is moved (via **Storage vMotion**) to a temporary **vVols** datastore located on a **Pure Storage FlashArray**.
- Each virtual disk is then **adopted** into OpenStack Cinder using the **Pure Storage Cinder driver**, utilizing the **volume group support** introduced in **OpenStack 2025.1 (Epoxy)**.

The temporary vVols datastore **must reside in an unstretched FlashArray Pod**. This ensures the Pure Storage Cinder driver can clone the volumes internally—enabling easy rollback and iterative fine-tuning by working on a cold copy of the original disks.

---

## 🧰 Requirements

Ensure the following Ansible collections and their dependencies are installed:

- `community.vmware`
- `purestorage.flasharray`
- `openstack.cloud`

> 📚 Please refer to the documentation for each collection for installation instructions and prerequisites.

---

## 🚀 Usage

1. All configuration variables are defined in:  
   `group_vars/all.yaml`

2. The inventory file (`inventory.ini`) includes a single target:  
   `localhost` (no changes needed)

3. To execute the playbook, run:

   ```bash
   ansible-playbook -i inventory.ini migrate_vms.yaml
   
### 🧩 Variables

| Variable name                | Description                                                                                    |
| ---------------------------- | ---------------------------------------------------------------------------------------------- |
| `vcenter_hostname`           | vCenter hostname/IP address                                                                    |
| `vcenter_username`           | vCenter account name                                                                           |
| `vcenter_password`           | vCenter account password (Use Ansible Vault in a real use case)                                |
| `vcenter_validate_certs`     | Enable/disable vCenter certificate validation (`true` or `false`)                              |
| `datacenter`                 | Name of the datacenter where the VMs are located                                               |
| `pure_fa_url`                | FlashArray management endpoint                                                                 |
| `temp_vvol_datastore_name`   | Temporary vVol datastore. Must be created in an unstretched FlashArray storage container (Pod) |
| `cinder_host_string`         | Cinder host in canonical format, e.g., `cinder-host@pure-iscsi#PureArray1-Pool`                |
| `cinder_volume_id_type`      | Cinder volume ID type. Default: `source-name`, uses volume name on the array for lookup        |
| `cinder_volume_type`         | OpenStack Cinder volume type                                                                   |
| `os_auth_url`                | OpenStack Identity (Keystone) endpoint                                                         |
| `os_user`                    | OpenStack user account                                                                         |
| `os_password`                | OpenStack user password (Use Ansible Vault in a real use case)                                 |
| `os_project`                 | OpenStack project name                                                                         |
| `os_domain`                  | OpenStack domain name                                                                          |
| `os_cloud`                   | OpenStack cloud name                                                                           |
| `os_default_flavor`          | Default flavor to use in OpenStack                                                             |
| `os_default_network`         | Default OpenStack network                                                                      |
| `os_default_keypair`         | Default SSH keypair in OpenStack                                                               |
| `os_default_security_groups` | Default security groups in OpenStack                                                           |
| `vms_to_migrate`             | List of virtual machines to be migrated                                                        |

#### 🖥️ Virtual Machine Format
Each VM to be migrated should follow this structure in the vms_to_migrate list:
| Variable name       | Description                     |
| ------------------- | ------------------------------- |
| `name`              | vSphere VM name                 |
| `os_instance_name`  | Target name for OpenStack VM    |
| `os_flavor`         | Flavor to assign in OpenStack   |
| `os_network`        | Network to connect in OpenStack |
| `os_keypair`        | SSH keypair to use              |
| `os_security_group` | Security group(s) to assign     |

## Demo

There is a short video in the `demo` directory that shows an actual execution of the playbook that migrates threel Ubuntu VMs, all representing a moderately comples scenario: a microk8s that runs a postgresql example deployment.

