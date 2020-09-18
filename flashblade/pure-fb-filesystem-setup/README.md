FlashBlade File System setup
=========

Ansible playbook and role for FlashBlade File System provisioning and configuration.


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
    $ ansible-galaxy collection install purestorage.flashblade:1.3.0 --force
    ```

Role Variables
--------------

There are two variable files "fb_details.yml" and "fb_secrets.yml" are holding the Ansible variables for the role at path `vars/<enviorement_name>`. 

This role and playbook can be used to setup network on FlashBlade servers in different environments. To store role variable files user can create different directories with `vars/<environment_name>`. User must specify `<environment_name>` while running `ansible-playbook` by specifying value in extra vars command line flag `-e "env=<environment_name>"`.

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
          fb_url: 10.12.231.151                    
          filesystem:
            - { name: database, count: 5, size: 32G, type: nfsv4.1, nfs_rules: '*(rw,no_root_squash)' } 
            - { name: tools, size: 1G, type: smb, nfs_rules: '*(rw,no_root_squash)' } 
          filesystem_snapshot: 
            - { filesystem_name: tools, suffix: ansible } # snap_name : tools.ansible
          filesystem_snapshot_policy:
            - { name: daily, at: 11AM, keep_for: 86400, every: 86400, timezone: Asia/Shanghai } # optional params: timezone
                       
    ```

* fb_secrets.yml
    ```
    array_secrets:               
      FBServer1:
        api_token: T-c61e4dec-xxxx-4264-87f8-315264d9e65a
    ```
#### Note
 * To destroy any of the filesystem use `state: disabled` in `fb_details.yml` variable file. Destroyed file systems have 24 hours to be recovered. To recover file system, run the playbook with `state: enabled` within 24 hours of deletion. Filesyetm can be eradicated by using `state: disabled` and `eradication: true` together. Eradicating a file system will also eradicate all of its related snapshots. 

   ##### fb_details.yml for different scenarios  
   
   **Create a File System**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.12.231.151                    
        filesystem:
          - { name: database, size: 32G, type: nfsv4.1, nfs_rules: '*(rw,no_root_squash)' }                         
   ```
 
   **Create 5 File Systems**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.12.231.151                    
        filesystem:
          - { name: database, count: 5 size: 32G, type: nfsv4.1, nfs_rules: '*(rw,no_root_squash)' } # creates 5 filesystem with name database_01....database_05.              
   ```    
   **Destroy File System**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.12.231.151                    
        filesystem:
          - { name: database, state: disabled }           
   ``` 
   **Recover File System**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.12.231.151                    
        filesystem:
          - { name: database, state: enabled }           
   ```
   **Eradicate File System**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.12.231.151                    
        filesystem:
          - { name: database, state: disabled, eradicate: true }           
   ``` 
   **Create File System snapshot**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.12.231.151                    
        filesystem_snapshot: 
          - { filesystem_name: tools, suffix: ansible } # snap_name : tools.ansible         
   ```
   **Destroy File System snapshot**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.12.231.151                    
        filesystem_snapshot: 
          - { filesystem_name: tools, suffix: ansible, state: disabled }
   ```
   **Recover File System snapshot**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.12.231.151                    
        filesystem_snapshot: 
          - { filesystem_name: tools, suffix: ansible, state: enabled }
   ```
   **Recover File System from latest snapshot**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.12.231.151                    
        filesystem_snapshot: 
          - { filesystem_name: tools, suffix: ansible, restore_fs_from_snap: true }
   ```
   **Eradicate File System snapshot**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.12.231.151                    
        filesystem_snapshot: 
          - { filesystem_name: tools, suffix: ansible, state: disabled, eradicate: true }
   ```
   **Create File System snapshot policy**
   ```
    array_inventory:               
    FBServer1:
      fb_url: 10.12.231.151                    
      filesystem_snapshot_policy:
        - { name: daily, at: 11AM, keep_for: 86400, every: 86400, timezone: Asia/Shanghai } # optional params: timezone
   ```
   **Delete File System snapshot policy**
   ```
    array_inventory:               
    FBServer1:
      fb_url: 10.12.231.151                    
      filesystem_snapshot_policy:
        - { name: daily, state: disabled } # optional params: timezone
   ```
 * To extend the File System provisioning on the fleet of FlashBlade Arrays, Add multiple "FBServer1...N" blocks under array_inventory in "fb_details.yml" file.
 Example configuration to setup DNS on two FlashBlade servers.
   
   **fb_details.yml**
   ```
   # FBServer details
    array_inventory:               
      FBServer1:
        fb_url: 10.xx.126.80
        filesystem:
          - { name: database, size: 32G, type: nfsv3 }   
      FBServer2:
        fb_url: 10.xx.126.110
        filesystem:
          - { name: tools, size: 32G, type: nfsv4.1 }  
    ```
    **fb_secrets.yml**
    ```
    array_secrets:               
      FBServer1:
        api_token: T-c61e4dec-xxxx-4264-87f8-315264d9e65a
      FBServer2:
        api_token: T-d88e4dec-xxxx-4222-87g3-315264d9e77a
    ```
Dependencies
------------

None

Example Playbook
----------------

      - name: FlashBlade filesystem setup
        hosts: "localhost"
        gather_facts: false
        vars_files:
        - "vars/{{ env }}/fb_details.yml"
        - "vars/{{ env }}/fb_secrets.yml"
        roles:
            - purefb_filesystem_setup

To execute playbook, issue the following command:
( Replace `<enviorement_name>` with the correct value )
   ```bash
   $ ansible-playbook filesystem_setup.yml -e "env=<enviorement_name>" --ask-vault-pass
   ```
Enter Ansible-Vault password which used to encrypt "fb_secrets.yml" file.
