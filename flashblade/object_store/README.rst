============
Instructions
============

This playbook is for Ansible 2.9+ with the FlashBlade Collection installed.

This simple playbook will create an s3 account, a user in that account and then a bucket in the account.
During the creation of the s3 user a remote access key is created and then exposed.

Running the playbook a second time will create a second access key for the user.

A maximum of 2 access keys are allowed per user, so after running this script twice there will be no attempt to create a new access key.

To execute the example playbook, issue the following command::

  $ ansible-playbook s3_examples.yaml
