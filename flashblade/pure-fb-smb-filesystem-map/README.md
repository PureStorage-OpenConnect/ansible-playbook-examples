FlashBlade NFS File System mount
=========

Ansible playbook and role for FlashBlade SMB File System mount on clients.


Requirements
------------
**Requires: Python >=2.7, <=3.6 on Ansible control node.**

As purity-fb SDK supports Python >=2.7, <=3.6, We need to ensure that Installed Python version on Ansible control Node must be >=2.7 and <=3.6.

* Install python-pip on Ansible control node.

  CentOS:
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
  MacOS
    ```bash
    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $ python get-pip.py --user
    ```
  For more details to install Ansible on MacOS, follow this [link](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-with-pip).
  
* Install dependencies from "requirements.txt"
    ```bash
    $ sudo pip install -r requirements.txt 
    ```
* Install Ansible Collection for Pure Storage FlashBlade
    ```bash
    $ ansible-galaxy collection install purestorage.flashblade
    ```

Windows host setup
------------------

To setup windows host for Ansible, refer to the Ansible [documentation](https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html).

This example playbook and assume that the `CredSSP` authentication protocol enabled on host/client. 

Role Variables
--------------

There are two variable files "fb_details.yml" and "fb_secrets.yml" are holding the Ansible variables for the role at path `vars/<enviorement_name>`. 

This role and playbook can be used to setup SMB File System on FlashBlade servers and mount on clients in different environments. To store role variable files user can create different directories with `vars/<environment_name>`. User must specify `<environment_name>` while running `ansible-playbook` by specifying value in extra vars command line flag `-e "env=<environment_name>"`.

Ansible playbooks require API token to connect to FlashBlade servers. API token can be obtained by connecting FlashBlade management VIP through ssh for a specific user and running the following purity command.
   ```
   $ ssh <pureuser>@<pure_fb_mgmt_ip>
   $ pureadmin list <username> --api-token -–expose
   ```
Enter "fb_url" and "api_token" obtained from FlashBlade in variable files.

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
        fb_url: 10.222.22.60                   
        filesystem:
          - { name: winbackup, size: 32G, type: smb, smb_aclmode: native } 

    ######################## Mount/Unmount Filesystem on client/host ########################
    windows_client_mount:
      mount1:
        server: { fb_name: FBServer1, fileshare: winbackup, data_vip: NFS-1 } 
        client: { hosts: win, mount_state: mount, drive_letter: Z }                       
    ```

* fb_secrets.yml
    ```
    array_secrets:               
      FBServer1:
        token: T-154d4220-xxxx-xxxx-8d64-fe7ea4f93499
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
          - purefb_smb_mount


To execute playbook, issue the following command:
( Replace `<enviorement_name>` and `<client_pass> `with the correct value )
   ```bash
   $ ansible-playbook filesystem_smb_mount.yml -e "env=<enviorement_name> ansible_password=<client_pass>" --ask-vault-pass
   ```
Enter Ansible-Vault password when prompted.

To see the mapped drive on interactive session, user need to reboot the system.