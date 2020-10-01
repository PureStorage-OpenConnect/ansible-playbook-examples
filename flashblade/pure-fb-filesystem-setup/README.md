FlashBlade File System provisioning and configuration
=========

Ansible playbook and role for FlashBlade File System provisioning and configuration.


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
    $ cd ansible-playbook-examples/flashblade/pure-fb-filesystem-setup/
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

Update "api_token" obtained from FlashBlade in "fb_secrets.yml" file and "fb_host" value with FlashBlade Management VIP in "fb_details.yml" 

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
      FlashBlade1: # this must match the identifier used for this FlashBlade in fb_details.yml
        api_token: T-0b8ad89c-xxxx-yyyy-85ed-28660EXAMPLE  # API token obtained from FlashBlade

For an example of an fb_secrets.yml file, see:
  ```
  vars/region/fb_secrets.yml
  ```

Specifying FlashBlade connection details and File System configuration
--------------

To configure your FlashBlade connection details and the File System details, snapshot and snapshot policies you would like to provision, create a file at:
  ```
  vars/<your_env_name>/fb_details.yml
  ```

The fb_details.yml file should look similar to this:
   ```
    ---
    array_inventory:
      FBServer1:
        fb_host: 10.12.231.151   # FlashBlade Management IP
        filesystem:
          - { name: database, count: 5, size: 32G, type: nfsv4.1, nfs_rules: '*(rw,no_root_squash)', policy: daily }
          - { name: tools, size: 1G, type: nfsv3, nfs_rules: '10.21.152.0/24(ro)', policy: weekly }
        filesystem_snapshot:
          - { filesystem_name: database, count: 5, suffix: ansible }
          - { filesystem_name: tools, suffix: ansible }  # snap_name : tools.ansible
        filesystem_snapshot_policy:
          - { name: daily, at: 11AM, keep_for: 86400, every: 86400, timezone: Asia/Shanghai } # optional params: timezone
          - { name: weekly, at: 10AM, keep_for: 604800, every: 604800, timezone: America/Los_Angeles }         
   ```

As an example of an fb_details.yml file, see:
  ```
  /vars/region/fb_details.yml
  ```

Running this playbook
--------------

To run this playbook, specify the playbook name and your environment name at the command line:
   ```bash
   ansible-playbook filesystem_setup.yml -e "env=<your_env_name>"
   ```

Using Ansible Vault to Encrypt FlashBlade Credentials
--------------

It is strongly recommended that you avoid storing FlashBlade API credentials in a plain text file.

You can use Ansible Vault to encrypt your FlashBlade API credentials using a password that can be specified later at the command line when running your playbook.

To encrypt the fb_secrets.yml file:
  ```
  ansible-vault encrypt fb_secrets.yml
  ```
Enter the same password when prompted to encrypt the file.

To execute a playbook using an encrypted fb_secrets.yml file:
   ```bash
   ansible-playbook filesystem_setup.yml -e "env=<your_env_name>" --ask-vault-pass
   ```
Enter Ansible Vault password that was used to encrypt "fb_secrets.yml" file.


Notes on using this playbook
--------------

 * To destroy any of the filesystem use `state: disabled` in `fb_details.yml` variable file. Destroyed file systems have 24 hours to be recovered. To recover file system, run the playbook with `state: enabled` within 24 hours of deletion. Filesyetm can be eradicated by using `state: disabled` and `eradication: true` together. Eradicating a file system will also eradicate all of its related snapshots. 

   ##### fb_details.yml for different scenarios  
   
   **Create a File System**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151   # FlashBlade Management IP                 
        filesystem:
          - { name: database, size: 32G, type: nfsv4.1, nfs_rules: '*(rw,no_root_squash)' }                         
   ```
 
   **Create 5 File Systems**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151    # FlashBlade Management IP          
        filesystem:
          - { name: database, count: 5 size: 32G, type: nfsv4.1, nfs_rules: '*(rw,no_root_squash)' } # creates 5 filesystem with name database_01....database_05.              
   ```    
   **Destroy File System**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151     # FlashBlade Management IP           
        filesystem:
          - { name: database, state: disabled }           
   ``` 
   **Recover File System**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151      # FlashBlade Management IP         
        filesystem:
          - { name: database, state: enabled }           
   ```
   **Eradicate File System**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151     # FlashBlade Management IP               
        filesystem:
          - { name: database, state: disabled, eradicate: true }           
   ``` 
   **Create File System snapshot**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151      # FlashBlade Management IP            
        filesystem_snapshot: 
          - { filesystem_name: tools, suffix: ansible } # snap_name : tools.ansible         
   ```
   **Create snapshot of the 5 File Systems created using count parameter**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151       # FlashBlade Management IP            
        filesystem_snapshot: 
          - { filesystem_name: database, count: 5, suffix: ansible }            
   ```   
   **Destroy File System snapshot**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151        # FlashBlade Management IP        
        filesystem_snapshot: 
          - { filesystem_name: tools, suffix: ansible, state: disabled }
   ```
   **Recover File System snapshot**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151         # FlashBlade Management IP             
        filesystem_snapshot: 
          - { filesystem_name: tools, suffix: ansible, state: enabled }
   ```
   **Recover File System from latest snapshot**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151         # FlashBlade Management IP      
        filesystem_snapshot: 
          - { filesystem_name: tools, suffix: ansible, restore_fs_from_snap: true }
   ```
   **Eradicate File System snapshot**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151          # FlashBlade Management IP        
        filesystem_snapshot: 
          - { filesystem_name: tools, suffix: ansible, state: disabled, eradicate: true }
   ```
   **Create File System snapshot policy**
   ```
    array_inventory:               
    FBServer1:
      fb_host: 10.12.231.151            # FlashBlade Management IP
      filesystem_snapshot_policy:
        - { name: daily, at: 11AM, keep_for: 86400, every: 86400, timezone: Asia/Shanghai } # optional params: timezone
   ```
   **Attach File System snapshot policy to the File System**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151           # FlashBlade Management IP    
        filesystem:
          - { name: database, policy: daily }                         
   ```
   **Detach File System snapshot policy to the File System**
   ```
    array_inventory:               
      FBServer1:
        fb_host: 10.12.231.151           # FlashBlade Management IP 
        filesystem:
          - { name: database, policy: daily, policy_state: absent }        
   ```
   **Delete File System snapshot policy**
   ```
    array_inventory:               
    FBServer1:
      fb_host: 10.12.231.151              # FlashBlade Management IP    
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
        fb_host: 10.xx.126.80  # FlashBlade Management IP
        filesystem:
          - { name: database, size: 32G, type: nfsv3 }   
      FBServer2:
        fb_host: 10.xx.126.110  # FlashBlade Management IP
        filesystem:
          - { name: tools, size: 32G, type: nfsv4.1 }  
    ```
    **fb_secrets.yml**
    ```
    array_secrets:               
      FBServer1:
        api_token: T-c61e4dec-xxxx-4264-87f8-315264d9e65a  # API Token obtained from FlashBlade
      FBServer2:
        api_token: T-d88e4dec-xxxx-4222-87g3-315264d9e77a  # API Token obtained from FlashBlade
    ```
