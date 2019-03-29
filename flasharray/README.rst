============
Instructions
============

These playbooks are for Ansible 2.6+

To use these example files you must add you own hostnames or IP addresses for the hosts to be provisioned into
the ``hossts.ini`` file.

Also ensure toy correclty set the ``fa_url`` and ``api_token`` values in the main YAML files to match
those of your FlashArray,

To execute the example playbooks, issue the following commands::

  $ ansible-playbook -i hosts.ini multihost_provisioning.yaml

and::

  $ ansible-playbook -i hosts.ini multihost_provisioning_cleanup.yaml
