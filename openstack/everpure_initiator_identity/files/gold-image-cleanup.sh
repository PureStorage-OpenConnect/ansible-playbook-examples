#!/usr/bin/env bash
# Run as the last step before sealing a compute/hypervisor gold image.
# Removes per-host initiator identity so every node generates its own on first boot.
# Pair with files/cloud-init-initiator-identity.yaml (or an equivalent first-boot role)
# so the files are regenerated deterministically on the node, not inherited from the image.
set -euo pipefail

rm -f /etc/iscsi/initiatorname.iscsi
rm -f /etc/nvme/hostnqn /etc/nvme/hostid
: > /etc/machine-id             # empty file => systemd generates a new one at boot
rm -f /var/lib/dbus/machine-id  # recreated at boot on most distributions

echo "Initiator identity cleared. Seal the image now."
