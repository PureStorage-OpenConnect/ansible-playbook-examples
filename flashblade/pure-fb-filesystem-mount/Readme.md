FlashBlade NFS File System mount
=========

Ansible playbook and role for FlashBlade NFS File System mount on linux clients.

Requirements
------------
**Requires: Python >=2.7, <=3.6 to be installed on the Ansible control node.**

The Python version on the Ansible control node must match the version required by the FlashBlade Python SDK (purity_fb): Python >=2.7, <=3.6

Configure Ansible control node - MacOS:
--------------
* Setup pyenv and install Pyhton v3.6.9.
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

Configure Ansible control node - Linux(CentOS/Ubuntu):
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
      FBServer1: # this must match the identifier used for this FlashBlade in fb_details.yml
        api_token: T-79ced0e5-xxxx-xxxx-8741-66482f04c6d1 # API token obtained from FlashBlade
      FBServer2:
        api_token: T-0b8ad89c-xxxx-xxxx-85ed-286607dc2cd2 # API token obtained from another FlashBlade

For an example of an fb_secrets.yml file, see:
  ```
  vars/region/fb_secrets.yml
  ```

Specifying FlashBlade connection details and NFS File System mount configuration
--------------

To configure your FlashBlade connection details and the File System mount details, create a file at:
  ```
  vars/<your_env_name>/fb_details.yml
  ```

The fb_details.yml file should look similar to this:
  ```
    array_inventory:               
      FBServer1:
        fb_host: 10.22.222.80                   
        filesystem:
          - { name: tools, size: 1T, type: nfsv4.1, nfs_rules: '10.21.152.0/24(ro,noatime)' } 
          - { name: scratch, size: 1T, type: nfsv3, nfs_rules: '*(ro,noatime)' } 
          - { name: database, size: 1T, type: nfsv3, nfs_rules: '*(rw)' }

    linux_client_mount:
      mount1:
        server: { fb_name: FBServer1, fileshare: tools, datavip_name: data-vip } 
        client: { hosts: dc, mount_state: mount, mount_point: /mnt/tools, opts: "rw,noatime" }
      mount2:
        server: { fb_name: FBServer1, fileshare: scratch, datavip_name: nfs-a04-data1 } 
        client: { hosts: dc, mount_state: mount, mount_point: /mnt/scratch, opts: "rw" }
      mount3:
        server: { fb_name: FBServer1, fileshare: database, datavip_name: nfs-a04-data1 }
        client: { hosts: dc, mount_state: mount, mount_point: /mnt/database, opts: "rw" }      
  ```

Note: To set nfs_rules, Provide NF rules in format `IP/subnet(opts)`.
Example: '10.21.152.0/24(ro,noatime)'

As an example of an fb_details.yml file, see:
  ```
  /vars/region/fb_details.yml
  ```

To eradicate and unmount File System, change `mount_state` to `umount` and add `destroy: true, eradicate: true` in fb_details.yml.

Example `fb_details.yml` to eradicate and unmount filesystem.

  ```
    array_inventory:               
      FBServer1:
        fb_host: 10.22.222.80                   
        filesystem:
          - { name: tools, destroy: true, eradicate: true, size: 1T, type: nfsv4.1, nfs_rules: '*(ro,noatime)' } 
          - { name: scratch, destroy: true, eradicate: true, size: 1T, type: nfsv3, nfs_rules: '*(ro,noatime)' } 
          - { name: database, destroy: true, eradicate: true, size: 1T, type: nfsv3, nfs_rules: '*(rw,noatime)' }

    linux_client_mount:
      mount1:
        server: { fb_name: FBServer1, fileshare: tools, datavip_name: data-vip } 
        client: { hosts: dc, mount_state: umount, mount_point: /mnt/tools, opts: "rw,noatime" }
      mount2:
        server: { fb_name: FBServer1, fileshare: scratch, datavip_name: nfs-a04-data1 } 
        client: { hosts: dc, mount_state: umount, mount_point: /mnt/scratch, opts: "rw" }
      mount3:
        server: { fb_name: FBServer1, fileshare: database, datavip_name: nfs-a04-data1 }
        client: { hosts: dc, mount_state: umount, mount_point: /mnt/database, opts: "rw" }      
  ```
File System configuration options:
* name: Filesystem Name
* destroy: Destroy File System ( default false )
* eradicate: Define whether to eradicate the filesystem on delete or leave in trash. ( default false)
* size: Volume size in M, G, T or P units( default size unlimited)
* type: Which protocol to enable ( nfsv3, nfsv4.1, smb )
* snapshot: Define whether a snapshot directory is enabled for the filesystem. ( default false )
* fastremove: Define whether the fast remove directory is enabled for the filesystem. ( default false)
* hard_limit: Define whether the capacity for a filesystem is a hard limit. ( default false )

Running this playbook
--------------

To run playbook with host ssh key, issue the following command:
( Replace `<ssh_user>` with host ssh user name and `<key_file_path>` with host private key file path )
   ```bash
   $ ansible-playbook filesystem_mount.yml -e "env=<your_env_name>" -i hosts.ini --key-file=<key_file_path> --ask-vault-pass 
   ```

To run playbook with host password( Not Recommended ), issue the following command:

   ```bash
   $ ansible-playbook filesystem_mount.yml -e "env=<your_env_name>" -i hosts.ini --ask-vault-pass --ask-pass --ask-become-pass
   ```
Enter Ansible-Vault password, hosts/clients ssh password and root password.

**Note:** If you are using MacOS as Ansible control node and using password to connect to remote hosts, SSH connection with password not supported.
The workaround for this limitation is to pass `-c paramiko` flag in ansible-playbook command. Install paramiko using `pip install paramiko`.
   ```bash
   $ sudo pip install paramiko
   $ ansible-playbook filesystem_mount.yml -e "env=region" -i hosts.ini --ask-vault-pass --ask-pass --ask-become-pass -c paramiko
   ```
