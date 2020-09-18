FlashBlade NFS File System mount
=========

Ansible playbook and role for FlashBlade NFS File System mount on clients.


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

Role Variables
--------------

There are two variable files "fb_details.yml" and "fb_secrets.yml" are holding the Ansible variables for the role at path `vars/<enviorement_name>`. 

This role and playbook can be used to setup File System on FlashBlade servers and mount on clients in different environments. To store role variable files user can create different directories with `vars/<environment_name>`. User must specify `<environment_name>` while running `ansible-playbook` by specifying value in extra vars command line flag `-e "env=<environment_name>"`.

Ansible playbooks require API token to connect to FlashBlade servers. API token can be obtained by connecting FlashBlade management VIP through ssh for a specific user and running the following purity command.
   ```
   $ ssh <pureuser>@<pure_fb_mgmt_ip>
   $ pureadmin list <username> --api-token -–expose
   ```
Update "api_token" obtained from FlashBlade in "fb_secrets.yml" file and "fb_url" value with FlashBlade Management VIP in "fb_details.yml".

Encrypt "fb_secrets.yml" using Ansible-Vault and enter password when prompted. This password is required to run playbook.
```
$ ansible-vault encrypt fb_secrets.yml
```

Update variables in `fb_details.yml` and `fb_secrets.yml` files to the desired values.

* fb_details.yml
    ```
    array_inventory:               
      FBServer1:
        fb_url: 10.22.222.80                   
        filesystem:
          - { name: tools, size: 1T, type: nfsv4.1, nfs_rules: '*(ro,noatime)' } 
          - { name: scratch, size: 1T, type: nfsv3, nfs_rules: '*(ro,noatime)' } 
          - { name: database, size: 1T, type: nfsv3, nfs_rules: '*(rw,noatime)' }

    linux_client_mount:
      mount1:
        server: { fb_name: FBServer1, fileshare: tools, data_vip: data-vip } 
        client: { hosts: dc, mount_state: mount, mount_point: /mnt/tools, opts: "rw,noatime" }
      mount2:
        server: { fb_name: FBServer1, fileshare: scratch, data_vip: nfs-a04-data1 } 
        client: { hosts: dc, mount_state: mount, mount_point: /mnt/scratch, opts: "rw" }
      mount3:
        server: { fb_name: FBServer1, fileshare: database, data_vip: nfs-a04-data1 }
        client: { hosts: dc, mount_state: mount, mount_point: /mnt/database, opts: "rw" }
                       
    ```

* fb_secrets.yml
    ```
    array_secrets:               
      FBServer1:
        api_token: T-79ced0e5-xxxx-xxxx-8741-66482f04c6d1
      FBServer2:
        api_token: T-0b8ad89c-xxxx-xxxx-85ed-286607dc2cd2 
    ```
Note: To unmount FIleSystem, User can change `mount_state: umount` variable in fb_details.yml file.

Dependencies
------------

None

Example Playbook
----------------

      - name: FlashBlade filesystem setup
        hosts: localhost
        gather_facts: false
        vars_files:
        - "vars/{{ env }}/fb_details.yml"
        - "vars/{{ env }}/fb_secrets.yml"
        roles:
          - purefb_filesystem_setup

      - name: Mount file share on hosts
        hosts: all
        gather_facts: true
        vars_files:
        - "vars/{{ env }}/fb_details.yml"
        - "vars/{{ env }}/fb_secrets.yml"
        roles:
          - purefb_nfs_mount

To execute playbook with host ssh key, issue the following command:
( Replace `<ssh_user>` with host ssh user name and `<key_file_path>` with host private key file path )
   ```bash
   $ ansible-playbook filesystem_mount.yml -e "env=<enviorement_name>" -i hosts.ini --user=<ssh_user> --key-file=<key_file_path> --ask-vault-pass 
   ```

To execute playbook with host password( Not Recommended ), issue the following command:
( Replace `<enviorement_name>` with the correct value )
   ```bash
   $ ansible-playbook filesystem_mount.yml -e "env=<enviorement_name>" -i hosts.ini --ask-vault-pass --ask-pass --ask-become-pass
   ```
Enter Ansible-Vault password, hosts/clients ssh password and root password.

**Note:** If you are using MacOS as Ansible control node and using password to connect to remote hosts, SSH connection with password not supported.
The workaround for this limitation is to pass `-c paramiko` flag in ansible-playbook command. Install paramiko using `pip install paramiko`.
