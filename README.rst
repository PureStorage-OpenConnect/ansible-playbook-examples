============
Introduction
============

This repository contains a number of simple Ansible playbooks using both the
URI and PUREFA modules to issue commands to a Pure Storage Arrays.

The following items are assumed by all playbooks:

-  The user has a working knowledge of Ansible and Ansible Playbooks

-  Minimum Ansible version is denoted by the directory name. Playbooks in these directories
   were tested on the named version. 

-  Your Pure Storage Array should be accessible from your local
   Ansible host.

-  You have obtained a privileged API token from the Pure Storage
   Array that will be used by the playbooks.

Playbooks are simple and do not use Ansible inventory files as they are for
informational and demonstrational purposes only.

FlashArray modules are natively included in Ansible and are obtained by installing
the latest Ansible package:


``#  pip install ansible``

FlashBlade modules will be available in Ansible 2.7, expected to release on
October 4, 2018. Until that time you can get this modules by installing the
latest 2.7 Release Candidtate code:


``# pip install ansible==2.7.0rc3 --user``

====================
FlashArray Playbooks
====================
Customizing Playbooks for your environment
------------------------------------------

**Playbooks using the URI module must include the following variables:**

-  ``arrayurl``

-  ``api_version``

-  ``array_token``

You must have these variables set correctly in your playbook to ensure 
correct operation.

The ``arrayurl`` is the Management VIP of your FlashArray. 

The ``api_version`` is recommended to be the highest version supported by 
your FlashArray's current Purity code version. You can check which API version
is deployed with your version of Purity by using the reference table in the
Pure Storage support website (https://support.purestorage.com/FlashArray/PurityOE/REST_API/REST_API_Reference_Guides).
You can also get the Reference Guide for your REST API version to help you
develop more Playbooks.

The ``array_token`` can be obtained from your FlashArray for specific users
using the GUI interface in **System -> Users -> API Tokens** and select **Show API Token** from the
gear icon next to the user you require the token for. You may also obtain the token
using the ``flasharray_get_token.yaml`` playbook example in the *2.2/flasharray* folder of this repo in which you must provide a valid username
and password.

**Playbooks using the PUREFA modules (Ansible 2.4 or higher) must contain the following variables:**

- ``fa_url``

- ``api_token``

where ``fa_url`` is the Management VIP of your FlashArray, and ``api_token`` is the same as ``array_token`` above.

It is adviseable to use these variables per play when working with multiple FlashArrays, however you may also
use environment variables to set these values externally to playbooks so they are not needed in the playbook.
This is useful when configuring only one FlashArray. 

The environment varaibles are:

- ``PUREFA_URL``

- ``PUREFA_API``

Running Playbooks using the URI module
======================================

After modifying your playbooks you can execute them by using::

  $ ansible-playbook <playbook-name>.yaml -e "<required parameters>"

The ``<required parameters>`` are defined in each playbook.

Running Playbooks using native modules
======================================

After modifying your playbooks you can execute them by using::

  $ ansible-playbook <playbook-name>.yaml
