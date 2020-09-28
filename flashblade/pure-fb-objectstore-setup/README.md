FlashBlade Object Store Account, User, and Bucket Configuration
=========

Ansible playbook for FlashBlade Object Store account, user, and bucket configuration.


Requirements
------------

**Requires: Python >=2.7, <=3.6 to be installed on the Ansible control node.**

The Python version on the Ansible control node must match the version required by the FlashBlade Python SDK (purity_fb): Python >=2.7, <=3.6

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
  MacOS
    ```bash
    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $ python get-pip.py --user
    ```
  For more details to install Ansible on MacOS, follow this [link](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-with-pip).
  
* Install dependencies using the "requirements.txt" in the directory of this README file. (This ensures that ansible, purity-fb, netaddr, and pytz are installed):
    ```bash
    $ sudo pip install -r requirements.txt 
    ```
* Install the FlashBlade Ansible Collection: 
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
  var/<your_env_name>/fb_secrets.yml
  ```
where <your_env_name> is a name you assign to a group of one or more FlashBlade arrays.

The fb_secrets.yml file should look like this:

    ---
    array_secrets:
      FlashBlade1: # this must match the identifier used for this FlashBlade in fb_details.yml
        api_token: T-0b8ad89c-xxxx-yyyy-85ed-28660EXAMPLE  # API token obtained from FlashBlade

    s3_ansible_vault_pass: somepassword   # Required in order to encrypt s3 secrets files at vars/<environment_name>/s3_secrets/


For an example of an fb_secrets.yml file, see:
  ```
  var/region/fb_secrets.yml
  ```

Specifying FlashBlade connection details and Object Store configuration
--------------

To configure your FlashBlade connection details and the Object Store account, user, and bucket names you would like to provision, create a file at:
  ```
  var/<your_env_name>/fb_details.yml
  ```

The fb_details.yml file should look similar to this:
  ```
    array_inventory:               
      FlashBlade1: # this must match the identifier used for this FlashBlade in fb_secrets.yml
        fb_host: 10.20.30.40
        object_store:
        - account: your-account
          users: 
            - { name: your-object-store-user, create_new_access_key: true }
          buckets: 
            - { name: your-bucket-name }                  
  ```

As an example of an fb_details.yml file, see:
  ```
  /var/region/fb_details.yml
  ```


Running this playbook
--------------

To run this playbook, specify the playbook name and your environment name at the command line:
   ```bash
   ansible-playbook object_store_setup.yml -e "env=<your_env_name>"
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
   ansible-playbook object_store_setup.yml -e "env=<your_env_name>" --ask-vault-pass
   ```
Enter Ansible Vault password that was used to encrypt "fb_secrets.yml" file.


Notes on using this playbook
--------------

#### Note
 * To destroy any of the bucket use `destroy_bucket: true` in "buckets" section of `fb_details.yml` variable file. Destroyed bucket have 24 hours to be recovered. To recover bucket, run the playbook with `recover_bucket: true` within 24 hours of deletion. Buckets can be eradicated by using `destroy_bucket: true` and `eradicate: true` together.


Examples
--------------
   ##### fb_details.yml for different scenarios  
   
   **Create Object-store Account, user and bucket**
   ```
    array_inventory:               
      FlashBlade1:
        fb_host: 10.22.222.151                 
        object_store:
        - account: account1
          users: 
            - { name: user1, create_new_access_key: true }
          buckets: 
            - { name: bucket1 }                          
   ```
   
   **Destroy Bucket**
   ```
    array_inventory:               
      FlashBlade1:
        fb_host: 10.22.222.151                 
        object_store:
        - account: account1
          buckets: 
            - { name: bucket1, destroy_bucket: true }                          
   ```
   **Recover Bucket**
   ```
    array_inventory:               
      FlashBlade1:
        fb_host: 10.22.222.151                 
        object_store:
        - account: account1
          buckets: 
            - { name: bucket1, recover_bucket: true }             
   ```
   **Eradicate Bucket**
   ```
    array_inventory:               
      FlashBlade1:
        fb_host: 10.22.222.151                 
        object_store:
        - account: account1
          buckets: 
            - { name: bucket1, destroy_bucket: true, eradicate: true }            
   ``` 
   **Create User with key**
   ```
    array_inventory:               
      FlashBlade1:
        fb_host: 10.22.222.151                 
        object_store:
        - account: account1
          users: 
            - { name: user1, create_new_access_key: true }        
   ```
   **Create User without key**
   ```
    array_inventory:               
      FlashBlade1:
        fb_host: 10.22.222.151                 
        object_store:
        - account: account1
          users: 
            - { name: user1, create_new_access_key: false }     
   ```
 * To extend the Object-store provisioning on the fleet of FlashBlade Arrays, Add multiple "FlashBlade1...N" blocks under array_inventory in "fb_details.yml" file.
 Example configuration to setup Object-Store on two FlashBlade servers.
   
   **fb_details.yml**
   ```
    array_inventory:               
      FlashBlade1:
        fb_host: 10.22.222.151                   
        object_store:
        - account: account1
          users: 
            - { name: user1 }
          buckets: 
            - { name: bucket1 }
      FlashBlade2:
        fb_host: 10.22.222.152                  
        object_store:
        - account: account2
          state: enabled
          users: 
            - { name: user2 }
          buckets: 
            - { name: bucket2 }  
    ```
    **fb_secrets.yml**
    ```
    array_secrets:               
      FlashBlade1:
        api_token: T-0b8ad89c-xxxx-yyyy-85ed-286607dc2cd2
      FlashBlade2:
        api_token: T-0b8ad822-xxxx-yyyy-85ed-286607dc2cd2
    
    s3_ansible_vault_pass: pureansible # Required to encrypt s3 secret files 
    ```

Other notes
--------------

* If creating S3 credentials for a user (`create_new_access_key: true`), s3_secrets will be stored in an encypted file with name `<account_name>_<user_name>.yml` at path `vars/<environment_name>/s3_secrets/`. Use ansible vault to decrypt the s3_secrets file(s).
   ```
   ansible-vault decrypt <s3_secrets_filename> --ask-vault-pass
   ```
   Enter vault password(`s3_ansible_vault_pass`) when prompted.

* A maximum of 2 access keys are allowed per user, so after running this playbook twice with `create_new_access_key: true` parameter, there will be no attempt to create a new access key.

* To enable versioning use `versioning: enabled` in fb_details buckets section. Versioning only can be suspended once enabled. Use `versioning: suspended` to suspend versioning.
Example fb_details with versioning enabled.
   ```
    array_inventory:               
      FlashBlade1:
        fb_host: 10.22.222.151                 
        object_store:
        - account: account1
          buckets: 
            - { name: bucket1, versioning: enabled }          
   ```
