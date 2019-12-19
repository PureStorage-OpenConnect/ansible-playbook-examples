============
Instructions
============

These playbooks require Ansible 2.9+ and the Pure Storage FlashArray Collections installed.

Required
========

 * 2 x FlashArray (source and destination) with iSCSI connectivity, on the same VLAN
 * FlashArray's capable of being connected in an ActiveCluster
 * Host with iSCSI connectivity on same VLAN as FlashArray iSCSI network
 * purestorage Python SDK installed on host running playbooks, ie ``pip install purestorage``

Pre-Requisites
==============

 * Update the ``mig-vars.yaml`` file with the correct ``fa_url`` and ``api_token`` information for the source and destination array
 * Ensure one iSCSI port for both the source and destination arrays are identified

To create the example volume used in the main migration run the follwoing playbook::

  # ansible-playbook prepare-vol.yaml

To better show that this process works with live data being accessed on the volume during the migration, issue the following command::

 # < /dev/urandom tr -dc "X" | head -c1000000000000000000 > /mnt/mig-test/test

Remeber to change the target file if you use a different value for ``mount_path`` in the ``mig-vars.yaml`` file.

To perform the actual data migration run::

  # ansible-playbook migrate-vol.yaml

To remove all parts of this demo after succesful completion run::

  # ansible-playbook cleanup-vol.yaml
