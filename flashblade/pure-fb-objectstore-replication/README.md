FlashBlade Object Replication
=========

Ansible playbook and role for FlashBlade Array to Array and Array to S3 target(AWS) Object Replication.

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
    $ cd ansible-playbook-examples/flashblade/pure-fb-objectstore-replication/
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


Specifying FlashBlade connection details and Object Store configuration
--------------

To configure your FlashBlade connection details and the Object Store account, user, and bucket names you would like to provision, create a file at:
  ```
  var/<your_env_name>/fb_details.yml
  ```
##### Case: 1 - Array to Array Object Replication

* fb_details.yml
   ```
    ---
    # FBServer details
    array_inventory:               
      FBServer1:
        fb_host: 10.21.241.151     #FlashBlade Management IP
      FBServer2:
        fb_host: 10.21.241.11      #FlashBlade Management IP     

    # FB-FB Replication
    S3Replication: 
      replication1: # FB-FB Replication
        common_params: { delete: false, repl_type: oneway, src_dst_repl_pause: false, dst_src_repl_pause: false }
        src: { server: FBServer1, replvip: 10.21.152.231, account: srcaccount, user: srcuser, bucket: srcbucket }
        dst: { server: FBServer2, replvip: 10.21.236.204, account: dstaccount, user: dstuser, bucket: dstbucket }
   ```

* fb_secrets.yml
    ```
    array_secrets:               
      FBServer1:
        api_token: T-c61e4dec-xxxx-4264-87f8-315264d9e65a # API Token obtained from FlashBlade
      FBServer2:
        api_token: T-79ced0e5-1d36-yyyy-8741-66482f04c6d1 # API Token obtained from FlashBlade
    ```

To delete account, bucket, user, replica-link use `delete: true` in fb_details.yml.
Example fb_details.yml to delete FB-FB Object replication:
   
   ```
    ---
    # FBServer details
    array_inventory:               
      FBServer1:
        fb_host: 10.21.241.151     #FlashBlade Management IP
      FBServer2:
        fb_host: 10.21.241.11      #FlashBlade Management IP     

    # FB-FB Replication
    S3Replication: 
      replication1: # FB-FB Replication
        common_params: { delete: true, repl_type: oneway, src_dst_repl_pause: false, dst_src_repl_pause: false }
        src: { server: FBServer1, replvip: 10.21.152.231, account: srcaccount, user: srcuser, bucket: srcbucket }
        dst: { server: FBServer2, replvip: 10.21.236.204, account: dstaccount, user: dstuser, bucket: dstbucket }
   ```

Note: To delete account, bucket, user, replica-link, Replication network and Array connection use `delete: true, delete_connection: true` in fb_details.yml.

##### Case: 2 - Array to S3(AWS) Object Replication

* fb_details.yml
    ```
    ---
    # FBServer details
    array_inventory:               
      FBServer1:
        fb_host: 10.xx.xxx.151     #FlashBlade Management IP
      FBServer2:
        fb_host: 10.xx.xxx.11      #FlashBlade Management IP     

    # FB-FB or FB-AWS replication
    S3Replication: 
      replication1: # FB-AWS Replication
        common_params: { delete: false, pause_repl: false }
        src: { server: FBServer1, replvip: 10.xx.xxx.231, account: awssrcaccount, user: srcuser36, bucket: srcbucketaws }
        dst: { server: s3.amazonaws.com, region: us-west-2, credential: aws1, bucket: awsdstbucket } # aws1 is defined in fb_secrets.yml
     ```

* fb_secrets.yml
    ```
    array_secrets:               
      FBServer1:
        api_token: T-c61e4dec-xxxx-4264-87f8-315264d9e65a # API Token obtained from FlashBlade

    s3_secrets:
      aws1:
        access_id: AKIA2OFGHJ436YHILJ7T
        access_key: WeQHJYJ+xxx+yyyyy/5T4AdvwS1kBQwPA8QIW6
    ```

To delete Account, user, src bucket and Replica-link, use `delete: true` in fb_details.yml.
Example fb_details.yml to delete FB-AWS Object replication:

   ```
    ---
    # FBServer details
    array_inventory:               
      FBServer1:
        fb_host: 10.xx.xxx.151     #FlashBlade Management IP
      FBServer2:
        fb_host: 10.xx.xxx.11      #FlashBlade Management IP     

    # FB-FB or FB-AWS replication
    S3Replication: 
      replication1: # FB-AWS Replication
        common_params: { delete: true, pause_repl: false }
        src: { server: FBServer1, replvip: 10.xx.xxx.231, account: awssrcaccount, user: srcuser36, bucket: srcbucketaws }
        dst: { server: s3.amazonaws.com, region: us-west-2, credential: aws1, bucket: awsdstbucket } # aws1 is defined in fb_secrets.yml
   ```
To delete Account, user, src bucket, dst(AWS) bucket, Replica-link, Replication Network and Array connection, use `delete: true, delete_aws_bucket: true, delete_connection: true`

Note: 
  * To set bucket lifecycle policy, Add `noncurrent_version_expiration_days: 7` parameter with desired value in "fb_details.yml" for the buckets created on FlashBlade. For the buckets created on AWS along with parameter `noncurrent_version_expiration_days: 7`, user can set `expiration_days: 6` for the current version of the bucket.
  
  **Example fb_details.yml with lifecycle policies**
   ```
    # FBServer details
    array_inventory:               
      FBServer1:
        fb_host: 10.16.126.80   # FlashBlade Management IP                            

    # FB-AWS object replication
    S3Replication: 
      replication1:
        src: { server: FBServer1, account: srcaccount, user: srcuser, bucket: srcbucket, noncurrent_version_expiration_days: 7 }
        dst: { server: s3.amazonaws.com, region: us-west-2, credential: aws1, bucket: pureawsbucket, expiration_days: 6, noncurrent_version_expiration_days: 7  }
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
   ansible-playbook object_replication.yml -e "env=<your_env_name>" --ask-vault-pass
   ```
Enter Ansible Vault password that was used to encrypt "fb_secrets.yml" file.


Running this playbook
--------

To execute the playbook, issue the following command:
   ```bash
   $ ansible-playbook object_replication.yml -e "env=<your_env_name>" --ask-vault-pass
   ```
Enter Ansible-Vault password when prompted.
