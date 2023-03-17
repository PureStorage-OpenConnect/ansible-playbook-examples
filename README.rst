============
Introduction
============

This repository contains a number of simple Ansible playbooks using both the
PUREFA and PUREFB modules to issue commands to Pure Storage FlashArrays or FlashBlades.

The following items are assumed by all playbooks:

-  The user has a working knowledge of Ansible and Ansible Playbooks

-  Minimum Ansible version is denoted in the README or the actual playbooks. 

-  Your Pure Storage FlashArray or FlashBlade should be accessible from your local
   Ansible host.

-  You have obtained a privileged API token from the Pure Storage
   FlashArray or FlashBlade that will be used by the playbooks.

FlashArray and FlashBlade modules are natively included in Ansible and are obtained by installing
the latest Ansible package:


``#  pip install ansible``


==============================================
FlashArray (incl. Cloud Block Store) Playbooks
==============================================
Customizing Playbooks for your environment
------------------------------------------

**Playbooks must contain the following variables:**

- ``fa_url``

- ``api_token``

where ``fa_url`` is the Management VIP of your FlashArray and ``api_token`` is obtained from a FlashArray for specific users
using the GUI interface in **Settings -> Users** and select **Show API Token...** from the 3 elipses on the right side of the
display, next to the user you require the token for. You may also get the ``api_token`` by executing the following Purity
command after using SSH to log directly onto the array:: 

  # pureadmin list <username> --api-token --expose

**Note:** You can only expose the API token for the username you re logged in as on both the GUI and the CLI.

It is adviseable to use these variables per play when working with multiple FlashArrays, however you may also
use environment variables to set these values externally to playbooks so they are not needed in the playbook.
This is useful when configuring only one FlashArray. 

The environment varaibles are:

- ``PUREFA_URL``

- ``PUREFA_API``

====================
FlashBlade Playbooks
====================
Customizing Playbooks for your environment
------------------------------------------

**Playbooks must contain the following variables:**

- ``fb_url``

- ``api_token``

where ``fb_url`` is the Management VIP of your FlashBlade and ``api_token`` is obtained from a FlashBlade for specific users
by running the following Purity command after using SSH to log directly onto the FlashBlade:: 

  # pureadmin list <username> --api-token --expose

**Note:** You can only expose the API token for the username you re logged in as.

It is adviseable to use these variables per play when working with multiple FlashBlades, however you may also
use environment variables to set these values externally to playbooks so they are not needed in the playbook.
This is useful when configuring only one FlashArray. 

The environment varaibles are:

- ``PUREFB_URL``

- ``PUREFB_API``

=================
Running Playbooks
=================

After modifying your playbooks you can execute them by using::

  $ ansible-playbook <playbook-name>.yaml

=================
Support Statement
=================

This Ansible Playbook is a GitHub contribution from Pure Storage Customers, Architects, System 
Engineers, and Developers. As it is open-sourced, support and answers to enquiry are provided 
under Best Efforts support by the Pure Portfolio Solutions Group, Open Source Integrations team. 
For feature requests and bugs please use GitHub Issues. We will address these as soon as we can, 
but there are no specific SLAs. In Addition, Pure Storage provide professional service to assist 
in its implementation and integration according to specific user requirement.