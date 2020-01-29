============
Instructions
============

This playbook is for Ansible 2.9+ with the FlashBlade Collection installed.

To use this example file you must add you own hostnames or IP addresses for the hosts to be provisioned into the ``hossts.ini`` file.

Also ensure you correclty set the ``url`` and ``api_token`` values in the YAML file to match those of your FlashBlade

To execute the example playbook, issue the following command::

  $ ansible-playbook -i hosts.ini nfs_multihost_mount.yaml
