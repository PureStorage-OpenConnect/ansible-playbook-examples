FlashBlade SMB FileSystem mapping on Windows clients 
=========

Ansible playbook and role for FlashBlade SMB File System mapping on Windows clients.


Requirements
------------
**Requires: Python >=2.7, <=3.6 to be installed on the Ansible control node.**

The Python version on the Ansible control node must match the version required by the FlashBlade Python SDK (purity_fb): Python >=2.7, <=3.6

Configure Ansible control node - MacOS
--------------
* Setup pyenv and install Python v3.6.9.
   ```bash
    $ brew install pyenv
    $ echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
    $ source ~/.bash_profile
    $ pyenv install 3.6.9
    $ pyenv global 3.6.9
   ```
* Check installed Python version, Output should be `Python 3.6.9`.
   ```bash
    $ python3 --version
   ```
* Clone Ansible Example Git Repository 
   ```bash
    $ git clone https://github.com/PureStorage-OpenConnect/ansible-playbook-examples.git
   ```
* Install dependencies using the “requirements.txt” in the directory of this README file. (This ensures that ansible, purity-fb, netaddr, and pytz are installed):
   ```bash
    $ cd ansible-playbook-examples/flashblade/pure-fb-sm-filesystem-map/
    $ pip3 install -r requirements.txt
   ```
    **Note:** Upgrading directly from ansible-2.9 or less to ansible-2.10 or greater with pip is not supported, Uninstall ansible-2.9 or less before installing ansible-2.10 or greater.
    ```bash
    $ pip uninstall ansible
    $ pip install ansible
    ```
* Install the FlashBlade Ansible Collection: ( Requires Ansible-2.10 or greater)
    ```bash
    $ ansible-galaxy collection install git+https://github.com/Pure-Storage-Ansible/FlashBlade-Collection.git#/collections/ansible_collections/purestorage/flashblade/ --force
    ```

Configure Ansible control node - Linux(CentOS/Ubuntu)
--------------

* Install python-pip on Ansible control node, if it is not already installed.

  CentOS/RHEL:
    ```bash
    $ sudo yum install epel-release
    $ sudo yum install python-pip
    $ sudo pip install --upgrade pip
    ```
  Ubuntu:
    ```bash
    $ sudo apt install python-pip
    $ sudo pip install --upgrade pip
    ```
  
* Install dependencies using the "requirements.txt" in the directory of this README file. (This ensures that ansible, purity-fb, netaddr, and pytz are installed):
    ```bash
    $ sudo pip install -r requirements.txt 
    ```
    **Note:** Upgrading directly from ansible-2.9 or less to ansible-2.10 or greater with pip is not supported, Uninstall ansible-2.9 or less before installing ansible-2.10 or greater.
    ```bash
    $ pip uninstall ansible
    $ pip install ansible
    ```
* Install the FlashBlade Ansible Collection: ( Requires Ansible-2.10 or greater)
    ```bash
    $ ansible-galaxy collection install git+https://github.com/Pure-Storage-Ansible/FlashBlade-Collection.git#/collections/ansible_collections/purestorage/flashblade/ --force
    ```

Windows host setup
------------------

To setup windows host for Ansible, refer to the Ansible [documentation](https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html).

For this playbook we assumes that the `CredSSP` authentication protocol enabled on host/client. 

Role Variables
--------------

There are two variable files "fb_details.yml" and "fb_secrets.yml" are holding the Ansible variables for the role at path `vars/<enviorement_name>`. 

This role and playbook can be used to setup SMB File System on FlashBlade servers and mount on clients in different environments. To store role variable files user can create different directories with `vars/<environment_name>`. User must specify `<environment_name>` while running `ansible-playbook` by specifying value in extra vars command line flag `-e "env=<environment_name>"`.

Ansible playbooks require API token to connect to FlashBlade servers. API token can be obtained by connecting FlashBlade management VIP through ssh for a specific user and running the following purity command.
   ```
   $ ssh <pureuser>@<pure_fb_mgmt_ip>
   $ pureadmin list <username> --api-token -–expose
   ```
Update "api_token" obtained from FlashBlade in "fb_secrets.yml" file and "fb_host" value with FlashBlade Management VIP in "fb_details.yml" 

Encrypt "fb_secrets.yml" using Ansible-Vault and enter password when prompted. This password is required to run playbook.
```
$ ansible-vault encrypt fb_secrets.yml
```

Update variables in `fb_details.yml` and `fb_secrets.yml` files to the desired values.

* fb_details.yml
    ```
    ############################ FB array object-store provisioning #############################
    array_inventory:               
      FBServer1:
        fb_host: 10.222.22.60                   
        filesystem:
          - { name: winbackup, size: 32G, type: smb, smb_aclmode: native } 

    ######################## Mount/Unmount Filesystem on client/host ########################
    windows_client_mount:
      mount1:
        server: { fb_name: FBServer1, fileshare: winbackup, data_vip: NFS-1 } 
        client: { hosts: win, mount_state: mapped, drive_letter: Z }                       
    ```
  Note: To unmap the fileshare, use `mount_state: unmapped` in "fb_details.yml" file.

* fb_secrets.yml
    ```
    array_secrets:               
      FBServer1:
        api_token: T-154d4220-xxxx-xxxx-8d64-fe7ea4f93499
    ```
* hosts.ini 
    ```
    [win]
    windows-host1 ansible_host=10.xx.xxx.96

    [win:vars]
    ansible_user=<DOMAIN>\<user_name>
    ansible_connection=winrm
    ansible_winrm_transport=credssp
    ansible_winrm_server_cert_validation=ignore
    ```


Dependencies
------------

None

Example Playbook
----------------

      - name: FlashBlade filesystem setup
        hosts: localhost
        vars_files:
        - "vars/{{ env }}/fb_details.yml"
        - "vars/{{ env }}/fb_secrets.yml"
        roles:
          - purefb_filesystem_setup

      - name: Mount SMB file share on windows hosts
        hosts: win
        gather_facts: false
        vars_files:
        - "vars/{{ env }}/fb_details.yml"
        - "vars/{{ env }}/fb_secrets.yml"
        roles:
          - purefb_smb_map


To execute playbook, issue the following command:
( Replace `<enviorement_name>` and `<client_pass> `with the correct value )
   ```bash
   $ ansible-playbook filesystem_smb_map.yml -e "env=<enviorement_name> ansible_password=<client_pass>" --ask-vault-pass
   ```
Enter Ansible-Vault password when prompted.

**Note:** To see the mapped drive on interactive session, user need to reboot the system.
