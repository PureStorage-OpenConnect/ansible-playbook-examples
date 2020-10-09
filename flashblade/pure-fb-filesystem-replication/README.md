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

Generating FlashBlade Login Credentials for Ansible Playbooks
--------------

FlashBlade Ansible playbooks require an API token to connect to FlashBlade. An API token can be obtained by using ssh to connect to the FlashBlade management IP for a user that you wish the Ansible playbook to run as, and using the ```pureadmin``` command to retrieve or create an API token.

To create or retrieve an API token, first ssh to a FlashBlade as the user you wish the Ansible playbooks to run as. For example, to create an API token with full admin privileges equivalent to "pureuser", the built-in local administrator account, ssh to FlashBlade's management IP as "pureuser" and specify that user's password:
   ```
   ssh pureuser@flashblade.example.com
   ```
To see current the logged-in user's API token:
   ```
   pureadmin list --api-token --expose
   ```
To create an API token expiring in 24 hours with the same permissions as the currently logged in user:
   ```
   pureadmin create --api-token --timeout 1d
   ```
The above commands generates output like the following:
   ```
   Name      API Token                               Created                  Expires
   pureuser  T-85cc9ce8-643d-4d99-8dbc-656f38cacab0  2020-09-13 23:55:33 PDT  2020-09-14 23:55:33 PDT
   ```
For details, see "Creating an API token" in the [FlashBlade User Guide](https://support.purestorage.com/FlashBlade/Purity_FB/FlashBlade_User_Guides).

Update "api_token" obtained from FlashBlade in "fb_secrets.yml" file and "fb_host" value with FlashBlade Management VIP in "fb_details.repl.yml" and "fb_details.fo_fb.yml" files. 

Specifying FlashBlade API credentials for this playbook
--------------

This playbook supports organizing your FlashBlade credentials and configuration details into groups of FlashBlade arrays referred to here as "environments".

To specify credentials for this playbook to log into FlashBlade, create a file (relative to this playbook's location) at
  ```
  vars/<your_env_name>/fb_secrets.yml
  ```
where <your_env_name> is a name you assign to a group of one or more FlashBlade arrays.

The fb_secrets.yml file should look like this:

    ---
    array_secrets:
      FlashBlade1: # this must match the identifier used for this FlashBlade in fb_details
        api_token: T-0b8ad89c-xxxx-yyyy-85ed-28660EXAMPLE  # API token obtained from FlashBlade
      FBServer2:
        api_token: T-79ced0e5-xxxx-xxxx-8741-66482f04c6d1  # API token obtained from FlashBlade

For an example of an fb_secrets.yml file, see:
  ```
  vars/region/fb_secrets.yml
  ```

Using Ansible Vault to Encrypt FlashBlade Credentials
--------------

It is strongly recommended that you avoid storing FlashBlade API credentials in a plain text file.

You can use Ansible Vault to encrypt your FlashBlade API credentials using a password that can be specified later at the command line when running your playbook.

To encrypt the fb_secrets.yml file:
  ```
  ansible-vault encrypt fb_secrets.yml
  ```
Enter password when prompted to encrypt the file.

Specifying FlashBlade connection details and Replication configuration
--------------

To configure your FlashBlade connection and Filesystem Replication details, create fb_details.repl.yml ( for failover/failback create file fb_details.fo_fb.yml ).

  ```
  var/<your_env_name>/fb_details.repl.yml
  var/<your_env_name>/fb_details.fo_fb.yml
  ```

Example fb_details for replication and failover/failback, see:

  ```
  var/region/fb_details.repl.yml
  vars/region/fb_details.fo_fb.yml
  ```

   #### Filesystem Replication 
   File system replication requires two connected arrays and a replica link between the source file system and a target file system. A replica link is the connection between a local file system and target file system.

   **fb_details.repl.yml for replication**
   
    # FlashBlade inventory
    array_inventory:               
      FBServer1:
        fb_host: 10.22.222.80    #FlashBlade Management IP 
        filesystem_snapshot_policy:
          - { name: daily, at: 12AM, keep_for: 86400, every: 86400, timezone: America/Los_Angeles }
      FBServer2:
          fb_host: 10.22.222.100  #FlashBlade Management IP

    # Filesystem replication
    FSReplication:       
      replication1:
        common_params: { repl_policy: daily }
        src: { fb_name: FBServer1, replvip: 10.21.152.231, fileshare: src-nfs }
        dst: { fb_name: FBServer2, replvip: 10.21.236.201 }             
   
`filesystem_snapshot_policy` variables:
* `name`: name of the policy
* `enabled`: whether policy is enabled( True/False )
* `every`: Frequency in which snapshots are created - Range( in seconds ) available 300 - 31536000 (equates to 5m to 365d)
* `at`: The time of day in which snapshots are created - Provide a time in 12-hour AM/PM format, eg. 11AM
* `timezone`: The timezone in which the snapshot is created( Used by `At` parameter ) - If not provided, the module will attempt to get the current local timezone from the server 
* `keep_for`: The period in which snapshots are retained until they are eradicated( Must not be set less than `every` ) - Range available 300 - 31536000 (equates to 5m to 365d)

Snapshot Policy Examples: 

* Daily: { name: daily, at: 11AM, every: 86400, keep_for: 86400  }

* Weekly: { name: weekly, at: 11AM, every: 604800, keep_for: 604800 }

* Hourly: { name: hourly, every: 3600, keep_for: 3600 }

 #### Filesystem failover 
   In a replication setup, failover requires promoting the file system on target (remote) array and then demoting the file system on the local (source) array.
    
   Note that when demoting the local file system, any writes performed since the last replication will be discarded. If a local snapshot was taken since last replication, demoting the file system requires that snapshot be destroyed and eradicated. The file system must either have no snapshots, or the most recent snapshot must be a replication snapshot.
  
   Enter Clients inventory detail in `hosts.ini`.
   Example fb_details for failover present at `vars/region/fb_details.fo_fb.yml`
  
  **fb_details.fo_fb.yml for failover**
   
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
        src: { fb_name: FBServer1, datavip_name: <srcdatavip_name>, fileshare: src-nfs }
        dst: { fb_name: FBServer2, datavip_name: <dstdatavip_name> }                        
   ``` 
 #### Filesystem failback/reprotect 
   Performing failback restores the original local/target relationship between arrays and file systems in a replication setup. During failback, once the remote file system is demoted and the local file system is promoted and clients redirected to the local file system, the original replication setup resumes; data is written to the local file system and then replicated to the remote file system.
   
   Update Client/host details in `hosts.ini`. 
   Example fb_details for failback present at `vars/region/fb_details.fo_fb.yml`

   **fb_details.fo_fb.yml for failback**
   
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
        src: { fb_name: FBServer1, datavip_name: <srcdatavip_name>, fileshare: src-nfs }
        dst: { fb_name: FBServer2, datavip_name: <dstdatavip_name> }                        
   ``` 

Running this playbook
--------------

To execute playbook, issue the following command:
* Replication
   ```bash
   $ ansible-playbook filesystem_replication.yml -e "env=<your_env_name>" --ask-vault-pass
   ```
* Failover

  Using Remote host SSH key(Replace `<ssh-key-path>` with ssh private key path)
     ```bash
   $ ansible-playbook filesystem_failover.yml -i hosts.ini -e "env=<your_env_name>" --ask-vault-pass --key-file=<ssh-key-path>
   ```
   Enter vault password when prompted.
  
  Using Remote host password(Not Recommended)
   ```bash
   $ ansible-playbook filesystem_failover.yml -i hosts.ini -e "env=<your_env_name>" --ask-vault-pass --ask-pass --ask-become-pass
   ```
   Enter vault password, hosts ssh password and root password.

* Failback

  Using Remote host SSH key(Replace `<ssh-key-path>` with ssh private key path)
     ```bash
   $ ansible-playbook filesystem_failback.yml -i hosts.ini -e "env=<your_env_name>" --ask-vault-pass --key-file=<ssh-key-path>
   ```
   Enter vault password when prompted.

  Using Remote host password(Not Recommended)
   ```bash
   $ ansible-playbook filesystem_failback.yml -i hosts.ini -e "env=<your_env_name>" --ask-vault-pass --ask-pass --ask-become-pass
   ```
   Enter vault password, hosts ssh password and root password.

**Note:** 
* If you are using MacOS as Ansible control node and using password to connect to remote hosts, SSH connection with password not supported.
The workaround for this limitation is to pass `-c paramiko` flag in ansible-playbook command. Install paramiko using `pip install paramiko`.

  **Replication**
   ```bash
   $ ansible-playbook filesystem_replication.yml -e "env=region" --ask-vault-pass
   ```

  **failover**
  
   ```bash
   $ pip install paramiko
   $ ansible-playbook filesystem_failover.yml -i hosts.ini -e "env=region" --ask-vault-pass --ask-pass --ask-become-pass -c paramiko
   ```
   Enter remote hosts ssh password, root password and ansible vault password.
   
  **failback**
  
   ```bash
   $ ansible-playbook filesystem_failback.yml -i hosts.ini -e "env=region" --ask-vault-pass --ask-pass --ask-become-pass -c paramiko
   ```
   Enter remote hosts ssh password, root password and ansible vault password.

* To configure hosts in parallel, User can set `forks` value in `ansible.cfg` file to the required value. 
