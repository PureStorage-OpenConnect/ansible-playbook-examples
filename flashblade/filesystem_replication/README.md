FlashBlade File System Replication, Failover and Failback/Reprotect
=========

Ansible playbooks and roles to perform FlashBlade File System Replication, Failover and Failback/Reprotect.

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

This role and playbook can be used to setup replication on FlashBlade servers in different environments. To store role variable files user can create different directories with `vars/<environment_name>`. User must specify `<environment_name>` while running `ansible-playbook` by specifying value in extra vars command line flag `-e "env=<environment_name>"`.

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
    # FlashBlade inventory
    array_inventory:               
      FBServer1:
          fb_url: 10.22.222.80
      FBServer2:
          fb_url: 10.22.222.100

    # Filesystem replication
    FSReplication:       
      replication1:
          common_params: { repl_policy: hourly }
          client_details:
            - hosts: dc
              mount_point: /mnt/var/src-nfs
          src: { fb_name: FBServer1, data_vip: srcdatavip, fileshare: src-nfs }
          dst: { fb_name: FBServer2, data_vip: dstdatavip }             
    ```

* fb_secrets.yml
    ```
    array_secrets:               
      FBServer1:
          token: T-c61e4dec-xxxx-xxxx-87f8-315264d9e65a
      FBServer2:
          token: T-79ced0e5-xxxx-xxxx-8741-66482f04c6d1 
    ```
 
 ##### Filesystem Replication 
   Filesystem replication required local(src) and remote(dst) FlashBlades should be connected and replica-link will be established between local filesystem and remote filesystem with replication policy. 
   **fb_details.yml for replication**
   ```
    # FlashBlade inventory
    array_inventory:               
      FBServer1:
          fb_url: 10.22.222.80
      FBServer2:
          fb_url: 10.22.222.100

    # Filesystem replication
    FSReplication:       
      replication1:
          common_params: { repl_policy: hourly }
          src: { fb_name: FBServer1, fileshare: src-nfs }
          dst: { fb_name: FBServer2 }                      
   ```
 
 ##### Filesystem failover 
   Filesystem failover required target(dst) filesystem to be promoted and all the clients must then be directed to the target array. The local file system is then demoted.
   **fb_details.yml for failover**
   Enter Clients detail in `hosts.ini` and use provide mount point and "host/group_name" under "client_details" section in `fb_details.yml` file.
   Data VIP is required to redirect clients from local to remote array.

   ```
    # FlashBlade inventory
    array_inventory:               
      FBServer1:
          fb_url: 10.22.222.80
      FBServer2:
          fb_url: 10.22.222.100

    # Filesystem replication
    FSReplication:       
      replication1:
          common_params: { repl_policy: hourly }
          client_details:
            - hosts: dc
              mount_point: /mnt/var/src-nfs
          src: { fb_name: FBServer1, data_vip: srcdatavip, fileshare: src-nfs }
          dst: { fb_name: FBServer2, data_vip: dstdatavip }                        
   ``` 
 ##### Filesystem failback/reprotect 
   Filesystem failback required to stop writes on the promoted remote file system, promoting source filesystem and redirecting all the clients to local filesystem. The remote file system is then demoted.
   **fb_details.yml for failover**
   Enter Clients detail in `hosts.ini` and provide details of mount point and "host/group_name" under "client_details" section in `fb_details.yml` file.
   Data VIP is required to redirect clients from local to remote array.
   
   ```
    # FlashBlade inventory
    array_inventory:               
      FBServer1:
          fb_url: 10.22.222.80
      FBServer2:
          fb_url: 10.22.222.100

    # Filesystem replication
    FSReplication:       
      replication1:
          common_params: { repl_policy: hourly }
          client_details:
            - hosts: dc
              mount_point: /mnt/var/src-nfs
          src: { fb_name: FBServer1, data_vip: srcdatavip, fileshare: src-nfs }
          dst: { fb_name: FBServer2, data_vip: dstdatavip }                        
   ``` 

Dependencies
------------

None

Example Playbook
----------------

* Filesystem Replication
     
     ```
      - name: FlashBlade filesystem setup
        hosts: "localhost"
        gather_facts: false
        vars_files:
        - "vars/{{ env }}/fb_details.yml"
        - "vars/{{ env }}/fb_secrets.yml"
        roles:
            - purefb_filesystem_setup
     ```

* Filesystem failover
     ```
      - name: FlashBlade filesystem failover
        hosts: all
        vars_files:
        - "vars/{{ env }}/fb_details.yml"
        - "vars/{{ env }}/fb_secrets.yml"
        roles:
            - purefb_filesystem_failover
     ```
* Filesystem failback
     ```
      - name: FlashBlade filesystem failback/Reprotect
        hosts: all
        vars_files:
        - "vars/{{ env }}/fb_details.yml"
        - "vars/{{ env }}/fb_secrets.yml"
        roles:
            - purefb_filesystem_failback
     ```
To execute playbook, issue the following command:
( Replace `<enviorement_name>` with the correct value )
* Replication
   ```bash
   $ ansible-playbook filesystem_replication.yml -e "env=<enviorement_name>" --ask-vault-pass
   ```
* Failover
   ```bash
   $ ansible-playbook filesystem_failover.yml -i hosts -e "env=<enviorement_name>" --ask-vault-pass -k -K
   ```
   Enter vault password, hosts ssh password and root password.

* Failback
   ```bash
   $ ansible-playbook filesystem_failback.yml -i hosts -e "env=<enviorement_name>" --ask-vault-pass -k -K
   ```
   Enter vault password, hosts ssh password and root password.
