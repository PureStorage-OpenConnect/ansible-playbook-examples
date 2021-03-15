# Install and Configure iSCSI and Provision Cloud Block Store Volumes using Ansible on AWS

### There are 2 main Ansible playbooks described in this document:

**Playbook 1 - base_install_linux.yaml**

The 1st playbook will perform a base installation and configuration of iSCSI on a newly provisioned cloud VM. Secondly on the Cloud Block Store array, a host and volume will be be automatically provisioned via API. This playbook will rely on the volume name and size as specified by the user via a command line parameter. The default hostname of the VM and a randomly generated IQN will be used to configure the Cloud Block Store host and attach the volume to the host. 

**Playbook 2 - provision_storage_linux.yaml**

The 2nd playbook may be used for provisioning additional Cloud Block Store volumes after the 1st playbook has been run. This playbook will provision additional storage volumes on the Cloud Block Store array, again relying on the volume name and size as specified by the user via a command line parameter. This playbook will then perform an iSCSI rescan on the VM to make visible the newly added multipath device. 

*Note: The user will need to mount the newly added storage volume prior to use.*


## Before you Begin:

### Provision Cloud Block Store on AWS

Retrive the Management IP Address from CloudFormation Output and Generate A Pure API Token.

- The Pure API Token can be created and retrived from the Cloud Block Store CLI or GUI.

### Install ansible on EC2 VM (control node).

This is where you will pull down the [ansible repo](https://github.com/aaronbadger/ansible.git) and run the ansible playbooks from. 

- The control node needs to have network connectivity to the Cloud Block Store management interface.

  - Ansible communicates with remote machines over the SSH protocol so be sure to allow inbound traffic on port 22.

See [Installing Ansible Control Node Requirements](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#control-node-requirements) for official documentation. 

### Install Install Purestorage python SDK and ansible-galaxy collection on EC2 VM (control node).

``pip3 install purestorage``

``ansible-galaxy collection install purestorage.flasharray``


### Install ansible on EC2 VM (managed node).

This can be done via AWS user data or after instance launch via ssh and CLI.

### Supported Linux OS - AWS:

Amazon Linux 2 AMI (HVM)
- Tested AMI = ami-0a36eb8fadc976275 (64-bit x86)
- Default User = ec2-user

SUSE Linux Enterprise Server 15 SP2 (HVM)
- Tested AMI = ami-0174313b5af8423d7 (64-bit x86)
- Default User = ec2-user

Ubuntu Server 18.04 LTS (HVM)
- Tested AMI = ami-0ac73f33a1888c64a (64-bit x86)
- Default User = ubuntu

### AWS User Data:

Specify The Below User Data in AWS during EC2 Launch. 

- These commands can also be executed via CLI after the EC2 Instance has been provisioned.

**Amazon Linux 2**
```
#!/bin/bash
sudo amazon-linux-extras install ansible2 -y
```

**SUSE Linux Enterprise Server 15 SP2**
```
#!/bin/bash
zypper ar https://download.opensuse.org/repositories/systemsmanagement/openSUSE_Leap_15.2/systemsmanagement.repo
zypper --gpg-auto-import-keys refresh
zypper --non-interactive --no-gpg-checks --quiet install ansible
```

**Ubuntu 18.04**
```
#!/bin/bash
apt update
apt install software-properties-common -y
apt-add-repository --yes --update ppa:ansible/ansible
apt install ansible -y
```
For additional help with installing ansible, reference [Installing Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) for official documentation. 

*Note: If installing ansible via user data at the time of compute provisioning, allow a few minutes for the ansible installation to complete prior to running ansible playbooks against the VM. To confirm if the ansible installation is complete, ssh into the VM and run ansible --version.*


## Install and Configure iSCSI

### Playbook:

base_install_linux.yaml

**Example command:**

``ansible-playbook -i '10.0.3.164,' -i 'cloudblockstore,' --private-key='/home/ubuntu/.ssh/privatekey.pem' -e 'cloud_initiator='10.0.3.164' fa_url='10.0.1.237' volname=vol1 size=1T pure_api_token='265be729-0ccc-f79b-abf8-f94422eeaf42' ansible_user=ubuntu' base_install_linux.yaml``

**Required CLI parameters:**

``-i ',<IP address of VM storage initiator to be configured>,'``

``-i ',cloudblockstore,'``

- This is hardcoded within the ansible playbooks to allow for command-line inventory definition. DO NOT MODIFY.

``--private-key='<private SSH key path usually specified during compute provisioning>'``

``cloud_initiator='<IP address of VM storage initiator to be configured>'``

``fa_url='<IP address of the cloudblock store management interface>``

``volname=<volname> ``

``size=<volsize>``

- A volname and size are required to perform the initial iSCSI connection to the CloudBlockStore target.

``pure_api_token=<Cloud Block Store API Token>``

- A Pure API Token can be created and retrived from the Cloud Block Store CLI or GUI.

``ansible_user=<default user for ssh access to host>``


## Provision Cloud Block Store Volumes

### Playbook:

provision_storage_linux.yaml

**Example command:**

``ansible-playbook -i '10.0.3.164,' -i 'cloudblockstore,' --private-key='/home/ubuntu/.ssh/privatekey.pem' -e 'cloud_initiator='10.0.3.164' fa_url='10.0.1.237' volname=volyes size=2T pure_api_token='265be729-0ccc-f79b-abf8-f94422eeaf42' ansible_user=ubuntu' provision_storage_linux.yaml``

**Required CLI parameters:**

Required CLI parameters:

``-i ',<IP address of VM storage initiator to be configured>,'``

``-i ',cloudblockstore,'``

- This is hardcoded within the ansible playbooks to allow for command-line inventory definition. DO NOT MODIFY.

``--private-key='<private SSH key path usually specified during compute provisioning>'``

``cloud_initiator='<IP address of VM storage initiator to be configured>'``

``fa_url='<IP address of the cloudblock store management interface>``

``volname=<volname>``

``size=<volsize>``

- Specify a new volname name and volume size to be provisioned from Cloud Block Store and connected to the host.

``pure_api_token=<Cloud Block Store API Token>``

- A Pure API Token can be created and retrived from the Cloud Block Store CLI or GUI.

``ansible_user=<default user for ssh access to host>``
