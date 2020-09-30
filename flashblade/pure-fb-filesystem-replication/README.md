FlashBlade File System Replication, Failover and Failback/Reprotect
=========

Ansible playbooks and roles to perform FlashBlade File System Replication, Failover and Failback/Reprotect.

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
    $ cd ansible-playbook-examples/flashblade/pure-fb-filesystem-replication/
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
* Set environment variable to allow Ansible to use fork before running any playbook.
    ```bash
    $ echo 'export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES' >> ~/.bash_profile
    $ source ~/.bash_profile
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

Role Variables
--------------

There are two variable files "fb_details.yml" and "fb_secrets.yml" are holding the Ansible variables for the role at path `vars/<enviorement_name>`. 

This role and playbook can be used to setup replication on FlashBlade servers in different environments. To store role variable files user can create different directories with `vars/<environment_name>`. User must specify `<environment_name>` while running `ansible-playbook` by specifying value in extra vars command line flag `-e "env=<environment_name>"`.

Ansible playbooks require API token to connect to FlashBlade servers. API token can be obtained by connecting FlashBlade management VIP through ssh for a specific user and running the following purity command.
   ```
   $ ssh <pureuser>@<pure_fb_mgmt_ip>
   $ pureadmin list <username> --api-token --expose
   ```
Update "api_token" obtained from FlashBlade in "fb_secrets.yml" file and "fb_host" value with FlashBlade Management VIP in "fb_details.yml".

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
        fb_host: 10.22.222.80    #FlashBlade Management IP 
        filesystem_snapshot_policy:
          - { name: daily, at: 12AM, keep_for: 86400, every: 86400, timezone: Asia/Shanghai } # optional params: timezone
      FBServer2:
        fb_host: 10.22.222.100   #FlashBlade Management IP

    # Filesystem replication
    FSReplication:       
      replication1:
        common_params: { repl_policy: daily }
        src: { fb_name: FBServer1, replvip: 10.21.152.231, fileshare: src-nfs }
        dst: { fb_name: FBServer2, replvip: 10.21.236.201 }             
    ```

* fb_secrets.yml
    ```
    array_secrets:               
      FBServer1:
        api_token: T-c61e4dec-xxxx-xxxx-87f8-315264d9e65a
      FBServer2:
        api_token: T-79ced0e5-xxxx-xxxx-8741-66482f04c6d1 
    ```
 `filesystem_snapshot_policy` variables:
* `name`: name of the policy
* `enabled`: whether policy is enabled( True/False )
* `every`: Frequency in which snapshots are created - Range available 300 - 31536000 (equates to 5m to 365d)
* `at`: The time of day in which snapshots are created - Provide a time in 12-hour AM/PM format, eg. 11AM
* `timezone`: The timezone in which the snapshot is created( Used by `At` parameter ) - If not provided, the module will attempt to get the current local timezone from the server 
* `keep_for`: The period in which snapshots are retained until they are eradicated( Must not be set less than `every` ) - Range available 300 - 31536000 (equates to 5m to 365d)
 
 #### Filesystem Replication 
   In Filesystem replication local(src) and remote(dst) FlashBlades should be connected state. Replica-link will be established between local filesystem and remote filesystem with replication policy. 
   
   **fb_details.yml for replication**
   
    
    # FlashBlade inventory
    array_inventory:               
      FBServer1:
        fb_host: 10.22.222.80    #FlashBlade Management IP 
        filesystem_snapshot_policy:
          - { name: daily, at: 12AM, keep_for: 86400, every: 86400, timezone: Asia/Shanghai } # optional params: timezone
      FBServer2:
          fb_host: 10.22.222.100   #FlashBlade Management IP

    # Filesystem replication
    FSReplication:       
      replication1:
        common_params: { repl_policy: daily }
        src: { fb_name: FBServer1, replvip: 10.21.152.231, fileshare: src-nfs }
        dst: { fb_name: FBServer2, replvip: 10.21.236.201 }             
    

 #### Filesystem failover 
   In Filesystem failover target(dst) filesystem to be promoted and all the clients must then be directed to the target array. The local file system is then demoted.
  
   Enter Clients inventory detail in `hosts.ini` and specify `mount_point` under "client_details" section in `fb_details.yml` file.
   Data VIP is required to redirect clients from local to remote array.
  
  **fb_details.yml for failover**
   
   ```
    # FlashBlade inventory
    array_inventory:               
      FBServer1:
          fb_host: 10.22.222.80  #FlashBlade Management IP
      FBServer2:
          fb_host: 10.22.222.100  #FlashBlade Management IP

    # Filesystem replication
    FSReplication:       
      replication1:
        common_params: { repl_policy: daily }
        client_details:
          - hosts: dc
            mount_point: /mnt/src-nfs
        src: { fb_name: FBServer1, datavip_name: srcdatavip, fileshare: src-nfs }
        dst: { fb_name: FBServer2, datavip_name: dstdatavip }                        
   ``` 
 #### Filesystem failback/reprotect 
   Filesystem failback required to stop writes on the promoted remote file system, promoting source filesystem and redirecting all the clients to local filesystem. The remote file system is then demoted.
   
   Enter Clients detail in `hosts.ini` and provide details of mount point and "host/group_name" under "client_details" section in `fb_details.yml` file.
   Data VIP is required to redirect clients from local to remote array.
   
   **fb_details.yml for failback**
   
   ```
    # FlashBlade inventory
    array_inventory:               
      FBServer1:
        fb_host: 10.22.222.80  #FlashBlade Management IP
      FBServer2:
        fb_host: 10.22.222.100  #FlashBlade Management IP

    # Filesystem replication
    FSReplication:       
      replication1:
        common_params: { repl_policy: daily }
        client_details:
          - hosts: dc
            mount_point: /mnt/var/src-nfs
        src: { fb_name: FBServer1, datavip_name: srcdatavip, fileshare: src-nfs }
        dst: { fb_name: FBServer2, datavip_name: dstdatavip }                        
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
  Using Remote host SSH key(Replace `<ssh-key-path>` with ssh private key path)
     ```bash
   $ ansible-playbook filesystem_failover.yml -i hosts -e "env=<enviorement_name>" --ask-vault-pass --key-file=<ssh-key-path>
   ```
   Enter vault password when prompted.
  
  Using Remote host password(Not Recommended)
   ```bash
   $ ansible-playbook filesystem_failover.yml -i hosts -e "env=<enviorement_name>" --ask-vault-pass --ask-pass --ask-become-pass
   ```
   Enter vault password, hosts ssh password and root password.

* Failback
  Using Remote host SSH key(Replace `<ssh-key-path>` with ssh private key path)
     ```bash
   $ ansible-playbook filesystem_failback.yml -i hosts -e "env=<enviorement_name>" --ask-vault-pass --key-file=<ssh-key-path>
   ```
   Enter vault password when prompted.

  Using Remote host password(Not Recommended)
   ```bash
   $ ansible-playbook filesystem_failback.yml -i hosts -e "env=<enviorement_name>" --ask-vault-pass --ask-pass --ask-become-pass
   ```
   Enter vault password, hosts ssh password and root password.

**Note:** 
* If you are using MacOS as Ansible control node and using password to connect to remote hosts, SSH connection with password not supported.
The workaround for this limitation is to pass `-c paramiko` flag in ansible-playbook command. Install paramiko using `pip install paramiko`.

  **failover**
  
   ```bash
   $ sudo pip install paramiko
   $ ansible-playbook filesystem_failover.yml -i hosts -e "env=region" --ask-vault-pass --ask-pass --ask-become-pass -c paramiko
   ```
   Enter remote hosts ssh password, root password and ansible vault password.
   
  **failback**
  
   ```bash
   $ sudo pip install paramiko
   $ ansible-playbook filesystem_failback.yml -i hosts -e "env=region" --ask-vault-pass --ask-pass --ask-become-pass -c paramiko
   ```
   Enter remote hosts ssh password, root password and ansible vault password.

* To configure hosts in parallel, User can set `forks` value in `ansible.cfg` file to the required value. 