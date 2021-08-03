FlashBlade SMB File System mapping on Windows clients 
=========

Ansible playbook and role for FlashBlade SMB File System mapping on Windows clients.


Requirements
------------
**Requires: Python >=2.7, >=3.4 to be installed on the Ansible control node.**

The Python version on the Ansible control node must match the version required by the FlashBlade Python SDK (purity_fb): Python >=2.7, >=3.4

Configure Ansible control node - MacOS
--------------
* Check Python version, Output should be Python >=2.7, >=3.4.
   ```bash
    $ python3 --version
   ```
* Clone Ansible Example Git Repository 
   ```bash
    $ git clone https://github.com/PureStorage-OpenConnect/ansible-playbook-examples.git
   ```
* Install dependencies using the “requirements.txt” in the directory of this README file. (This ensures that ansible, purity-fb, netaddr, and pytz are installed):
   ```bash
    $ cd ansible-playbook-examples/flashblade/pure-fb-objectstore-replication/
    $ pip3 install -r requirements.txt
   ```
    **Note:** Upgrading directly from ansible-2.9 or less to ansible-2.10 or greater with pip is not supported, Uninstall ansible-2.9 or less before installing ansible-2.10 or greater.
    ```bash
    $ pip uninstall ansible
    $ pip install ansible
    ```
* Install the FlashBlade Ansible Collection:
    ```bash
    $ ansible-galaxy collection install purestorage.flashblade
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
* Install the FlashBlade Ansible Collection:
    ```bash
    $ ansible-galaxy collection install purestorage.flashblade
    ```

Windows host setup
------------------

To setup windows host for Ansible, refer to the Ansible [documentation](https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html).

For this playbook we assumes that the `CredSSP` authentication protocol enabled on host/client. 

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
  var/<your_env_name>/fb_secrets.yml
  ```
where <your_env_name> is a name you assign to a group of one or more FlashBlade arrays.

The fb_secrets.yml file should look like this:

    ---
    array_secrets:
      FBServer1: # this must match the identifier used for this FlashBlade in fb_details.yml
        api_token: T-0b8ad89c-xxxx-yyyy-85ed-28660EXAMPLE  # API token obtained from FlashBlade

For an example of an fb_secrets.yml file, see:
  ```
  var/region/fb_secrets.yml
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

To edit encrypted fb_secrets.yml file:
  ```
  ansible-vault edit fb_secrets.yml
  ```
Enter the same password when prompted to encrypt the file.


Specifying FlashBlade connection details and host details
--------------

To configure your FlashBlade connection details and the Object Store account, user, and bucket names you would like to provision, create a file at:
  ```
  var/<your_env_name>/fb_details.yml
  ```

The fb_details.yml file should look similar to this:
  ```
    ########################## FB array SMB File System provisioning #######################
    array_inventory:               
      FBServer1:
        fb_host: 10.222.22.60   # FlashBlade Management IP                
        filesystem:
          - { name: winbackup, size: 32G, type: smb, smb_aclmode: native } 

    ######################## Map/Unmap SMB Filesystem on client/host ########################
    windows_client_mount:
      mount1:
        server: { fb_name: FBServer1, fileshare: winbackup, data_vip: NFS-1 } 
        client: { hosts: win, map_state: mapped, reboot: true, drive_letter: Z }                  
  ```
Windows host should be rebooted to apply changes. User can specify `reboot: true` to reboot host machine along with `map_state: mapped`.

As an example of an fb_details.yml file, see:
  ```
  /var/region/fb_details.yml
  ```

Update `hosts.ini` with windows host IP and username. 

   ```
    [win]
    windows-host1 ansible_host=10.xx.xxx.96

    [win:vars]
    ansible_user=<DOMAIN>\<user_name>
    ansible_connection=winrm
    ansible_winrm_transport=credssp
    ansible_winrm_server_cert_validation=ignore
   ```

To eradicate and unmap SMB File System, change `map_state` to `unmapped` and add `destroy: true, eradicate: true` in fb_details.yml.

Example `fb_details.yml` to eradicate and unmap filesystem.

  ```
    ########################## FB array SMB File System provisioning #######################
    array_inventory:               
      FBServer1:
        fb_host: 10.222.22.60   # FlashBlade Management IP                
        filesystem:
          - { name: winbackup, destroy: true, eradicate: true, size: 32G, type: smb, smb_aclmode: native } 

    ######################## Map/Unmap Filesystem on client/host ########################
    windows_client_mount:
      mount1:
        server: { fb_name: FBServer1, fileshare: winbackup, data_vip: NFS-1 } 
        client: { hosts: win, map_state: unmapped, reboot: true, drive_letter: Z }                  
  ```     
Windows host should be rebooted to apply changes. User can specify `reboot: true` to reboot host machine along with `map_state: unmapped`.


Running this playbook
--------------

To execute playbook, issue the following command:
( Replace `<enviorement_name>` and `<client_pass> `with the correct value )
   ```bash
   $ ansible-playbook filesystem_smb_map.yml -e "env=<enviorement_name> ansible_password=<client_pass>" -i hosts.ini --ask-vault-pass
   ```
Enter Ansible-Vault password when prompted.

**Note:** To see the mapped drive on interactive session, user need to reboot the system.
