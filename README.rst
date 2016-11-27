Introduction
============

This irepository contains a number of simple Ansible playbooks using the URI 
module to issue commands to a Pure Storage FlashArray utilizing the FlashArray
RestAPI interface.

The following items are assumed by all playbooks:

-  The user has a working knowledge of Ansible and Ansible Playbooks

-  Ansible 2.2 or higher is used. These playbooks were tested on this version. 

-  Your Pure Storage FlashArray should be accessible from your local
   Ansible host.

-  You have obtained a privileged API token from the Pure Storage
   FlashArray that will be used by the playbooks.

Playbooks will be simple and not use Inventory files as there are for
informative and demonstration purposes only.

Customizing Playbooks for your environment
==========================================

All Playbooks include the following variables:

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
You can also get the Reference Guide for your ReastAPI version to help you
develop more Playbooks.

The ``array_token`` get be obtained from your FlashArray for specific users
using the GUI interface in **System -> Users -> API Tokens** and select **Show API Token** from the
gear icon next to the user you require the token for. You may also obtain the token
using the get-token.yaml playbook example in this repo in which you must provide a valid username
and password.

Running Playbooks
=================

After modifying your playbooks you can execute them by using::

  $ ansible-playbook <playbook-name>.yaml -e "<required parameters>"

The ``<required parameters>`` are defined in each playbook.
