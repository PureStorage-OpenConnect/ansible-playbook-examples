FlashBlade NFS File System mount
=========

Ansible playbook and role for FlashBlade nfs File System mount on clients.


Requirements
------------

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
Enter "fb_url" and "api_token" obtained from FlashBlade in variable files.

Encrypt "fb_secrets.yml" using Ansible-Vault and enter password when prompted. This password is required to run playbook.
```
$ ansible-vault encrypt fb_secrets.yml
```

Update variables in `fb_details.yml` and `fb_secrets.yml` files to the desired values.

* fb_details.yml
    ```
    ##################### FB array filesystem and object-store provisioning ##################
    array_inventory:               
      FBServer1:
        fb_url: 10.22.222.80                   
        filesystem:
          - { name: tools, size: 1T, type: nfsv4, nfs_rules: '*(ro,noatime)'  } 
          - { name: scratch, size: 1T, type: nfsv3, nfs_rules: '*(ro,noatime)' } 
          - { name: database, size: 1T, type: [nfsv3 , nfsv4], nfs_rules: '*(rw,noatime)' }

    ######################## Mount/Unmount Filesystem on client/host ########################
    linux_client_mount:
      mount1:
        server: { fb_name: FBServer1, fileshare: nfs-fs-dst, data_vip: data-vip } 
        client: { hosts: dc, mount_state: mount, mount_point: /mnt/var/tools, opts: rw,noatime }
      mount2:
        server: { fb_name: FBServer1, fileshare: scratch, data_vip: nfs-a04-data1 } 
        client: { hosts: host2, mount_state: mount, mount_point: /mnt/var/scratch, opts: rw }
      mount3:
        server: { fb_name: FBServer1, fileshare: database, data_vip: nfs-a04-data1 }
        client: { hosts: host3, mount_state: mount, mount_point: /mnt/var/database, opts: rw }
                       
    ```

* fb_secrets.yml
    ```
    array_secrets:               
      FBServer1:
        api_token: T-79ced0e5-xxxx-xxxx-8741-66482f04c6d1
      FBServer2:
        api_token: T-0b8ad89c-xxxx-xxxx-85ed-286607dc2cd2 
    ```

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

To execute playbook, issue the following command:
( Replace `<enviorement_name>` with the correct value )
   ```bash
   $ ansible-playbook filesystem_mount.yml -e "env=<enviorement_name>" --ask-vault-pass -k -K
   ```
Enter Ansible-Vault password, clients ssh password and root password.
