FlashBlade Obect-Store setup
=========

Ansible playbook and role for FlashBlade Object-Store provisioning and configuration.


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

There are two variable files "fb_details.yml" and "fb_secrets.yml" are holding the Ansible variables for the role at path `vars/<environment_name>`.

This role and playbook can be used to setup object-store on FlashBlade servers in different environments. To store role variable files user can create different directories with `vars/<environment_name>`. User must specify `<environment_name>` while running `ansible-playbook` by specifying value in extra vars command line flag `-e "env=<environment_name>"`.

Ansible playbooks require API token to connect to FlashBlade servers. API token can be obtained by connecting FlashBlade management VIP through ssh for a specific user and running the following purity command.
   ```
   $ ssh <pureuser>@<pure_fb_mgmt_ip>
   $ pureadmin list <username> --api-token --expose
   ```
Update "api_token" obtained from FlashBlade in "fb_secrets.yml" file and "fb_url" value with FlashBlade Management VIP in "fb_details.yml" 

Encrypt "fb_secrets.yml" using Ansible-Vault and enter password when prompted. This password is required to run playbook. To encrypt s3 secrets file, set `s3_ansible_vault_pass` variable in "fb_secrets.yml".   
```
$ ansible-vault encrypt fb_secrets.yml
```

Update variables in `fb_details.yml` and `fb_secrets.yml` files to the desired values.

* fb_details.yml
    ```
    array_inventory:               
      FBServer1:
        fb_url: 10.22.222.151                   
        object_store:
        - account: logaccount
          state: enabled
          users: 
            - {name: loguser, create_new_access_key: true, state: enabled}
          buckets: 
            - {name: logbucket, state: enabled, eradicate: false, versioning: enabled}                  
    ```

* fb_secrets.yml
    ```
    ---
    array_secrets:               
      FBServer1:
        api_token: T-0b8ad89c-xxxx-yyyy-85ed-286607dc2cd2  # api_token obtained from fb_server

    # Required to encrypt s3 secret files 
    s3_ansible_vault_pass: pureansible
    ```

#### Note
 * To destroy any of the bucket use `state: disabled` in "buckets" section of `fb_details.yml` variable file. Destroyed bucket have 24 hours to be recovered. To recover bucket, run the playbook with `state: enabled` within 24 hours of deletion. Buckets can be eradicated by using `state: disabled` and `eradicate: true` together.

   ##### fb_details.yml for different scenarios  
   
   **Create Object-store Account, user and bucket**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.22.222.151                 
        object_store:
        - account: logaccount
          state: enabled
          users: 
            - { name: loguser, create_new_access_key: true, state: enabled }
          buckets: 
            - { name: logbucket, state: enabled, eradicate: false, versioning: enabled }                          
   ```
   
   **Destroy Bucket**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.22.222.151                 
        object_store:
        - account: logaccount
          buckets: 
            - { name: logbucket, state: disabled }                          
   ```
   **Recover Bucket**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.22.222.151                 
        object_store:
        - account: logaccount
          buckets: 
            - { name: logbucket, state: enabled }             
   ```
   **Eradicate Bucket**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.22.222.151                 
        object_store:
        - account: logaccount
          buckets: 
            - { name: logbucket, state: disabled, eradicate: true }            
   ``` 
   **Create User with key**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.22.222.151                 
        object_store:
        - account: logaccount
          users: 
            - { name: loguser, create_new_access_key: true }        
   ```
   **Create User without key**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.22.222.151                 
        object_store:
        - account: logaccount
          users: 
            - { name: loguser, create_new_access_key: false }     
   ```
 * To extend the Object-store provisioning on the fleet of FlashBlade Arrays, Add multiple "FBServer1...N" blocks under array_inventory in "fb_details.yml" file.
 Example configuration to setup Object-Store on two FlashBlade servers.
   
   **fb_details.yml**
   ```
    array_inventory:               
      FBServer1:
        fb_url: 10.22.222.151                   
        object_store:
        - account: logaccount
          state: enabled
          users: 
            - { name: loguser, create_new_access_key: true, state: enabled }
          buckets: 
            - { name: logbucket, state: enabled, eradicate: false, versioning: enabled }
      FBServer1:
        fb_url: 10.22.222.152                  
        object_store:
        - account: srcaccount
          state: enabled
          users: 
            - { name: srcuser, create_new_access_key: true, state: enabled }
          buckets: 
            - { name: srcbucket, state: enabled, eradicate: false, versioning: enabled }  
    ```
    **fb_secrets.yml**
    ```
    array_secrets:               
      FBServer1:
        api_token: T-0b8ad89c-xxxx-yyyy-85ed-286607dc2cd2
      FBServer2:
        api_token: T-0b8ad822-xxxx-yyyy-85ed-286607dc2cd2
    # Required to encrypt s3 secret files 
    s3_ansible_vault_pass: pureansible
    ```
* If user created with key (`create_new_access_key: true`), s3_secrets will be stored in a encypted file with name `<account_name>_<user_name>.yml` at path `vars/<environment_name>/s3_secrets/` . Use ansible vault to decrypt the s3_secrets files.
   ```
   ansible-vault decrypt <s3_secrets_filename> --ask-vault-pass
   ```
   Enter vault password(`s3_ansible_vault_pass`) when prompted.
* Maximum of 2 access keys are allowed per user, so after running this playbook twice with `create_new_access_key: true` parameter there will be no attempt to create a new access key.

Dependencies
------------

None

Example Playbook
----------------
    ---
    - name: FlashBlade object-store setup
      hosts: localhost
      gather_facts: false
      vars_files:
      - "vars/{{ env }}/fb_details.yml"
      - "vars/{{ env }}/fb_secrets.yml"
      roles:
        - purefb_object_store_setup

To execute playbook, issue the following command:
( Replace `<environment_name>` with the correct value )
   ```bash
   $ ansible-playbook object_store_setup.yml -e "env=<environment_name>" --ask-vault-pass
   ```
Enter Ansible-Vault password which used to encrypt "fb_secrets.yml" file.
