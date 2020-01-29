============
Instructions
============

This playbook is for Ansible 2.9+ with the FlashBlade Collection installed.

To use this example file you must add you own hostnames or IP addresses for the hosts to be provisioned into the ``hossts.ini`` file.

Also ensure you correclty set the ``url``, ``api_token`` and other ``vars` values in the YAML file to those for your environment.

To execute the example playbook, issue the following command::

  $ ansible-playbook -i hosts.ini nfs_multihost_mount.yaml
