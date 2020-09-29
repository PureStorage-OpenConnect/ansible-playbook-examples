FlashBlade Object Replication
=========

Ansible playbook and role for FlashBlade Array to Array and Array to S3 target(AWS) object Replication.

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

Ansible playbooks require API token to connect to FlashBlade servers. API token can be obtained by connecting FlashBlade management VIP through ssh for a specific user and running the following purity command.
   ```
   $ ssh <pureuser>@<pure_fb_mgmt_ip>
   $ pureadmin list <username> --api-token --expose
   ```
Update "api_token" obtained from FlashBlade in "fb_secrets.yml" file and "fb_host" value with FlashBlade Management VIP in "fb_details.yml" 

Encrypt "fb_secrets.yml" using Ansible-Vault.
```
$ ansible-vault encrypt fb_secrets.yml
```

##### Case: 1 - Array to Array Object Replication

* fb_details.yml
   ```
   # FBServer details
    array_inventory:               
      FBServer1:
        fb_host: 10.xx.126.80
      FBServer2:
        fb_host: 10.yy.120.100                                    

    # FB-FB object replication
    S3Replication: 
      replication1:
        src: { server: FBServer1, account: srcaccount, user: srcuser, bucket: srcbucket }
        dst: { server: FBServer2, account: dstaccount, user: dstuser, bucket: dstbucket }
   ```

* fb_secrets.yml
    ```
    array_secrets:               
      FBServer1:
        api_token: T-c61e4dec-xxxx-4264-87f8-315264d9e65a
      FBServer2:
        api_token: T-79ced0e5-1d36-yyyy-8741-66482f04c6d1 
    ```
##### Case: 2 - Array to S3(AWS) Object Replication

* fb_details.yml
    ```
    # FBServer details
    array_inventory:               
      FBServer1:
        fb_host: 10.16.126.80                                  

    # FB-AWS object replication
    S3Replication: 
      replication1:
        src: { server: FBServer1, account: srcaccount, user: srcuser, bucket: srcbucket }
        dst: { server: s3.amazonaws.com, region: us-west-2, credential: aws1, bucket: awsdstbucket }
   ```

* fb_secrets.yml
    ```
    array_secrets:               
      FBServer1:
        api_token: T-c61e4dec-xxxx-4264-87f8-315264d9e65a

    s3_secrets:
      aws1:
        access_id: AKIA2OFGHJ436YHILJ7T
        access_key: WeQHJYJ+xxx+yyyyy/5T4AdvwS1kBQwPA8QIW6
    ```

Note: 
  * To set bucket lifecycle policy, Add `noncurrent_version_expiration_days: 7` parameter with desired value in "fb_details.yml" for the buckets created on FlashBlade. For the buckets created on AWS along with parameter `noncurrent_version_expiration_days: 7`, user can set `expiration_days: 6` for the current version of the bucket.
  **Example fb_details.yml with lifecycle policies**
   ```
    # FBServer details
    array_inventory:               
      FBServer1:
        fb_host: 10.16.126.80                                  

    # FB-AWS object replication
    S3Replication: 
      replication1:
        src: { server: FBServer1, account: srcaccount, user: srcuser, bucket: srcbucket, noncurrent_version_expiration_days: 7 }
        dst: { server: s3.amazonaws.com, region: us-west-2, credential: aws1, bucket: pureawsbucket, expiration_days: 6, noncurrent_version_expiration_days: 7  }
   ```


Dependencies
------------

None

Example Playbook
----------------

    - name: FlashBlade object-store replication
      hosts: localhost
      gather_facts: false
      vars_files:
      - "vars/{{ env }}/fb_details.yml"
      - "vars/{{ env }}/fb_secrets.yml"
      roles:
        - purefb_object_replication

To execute the playbook, issue the following command:
( Replace `<enviorement_name>` with the correct value )
   ```bash
   $ ansible-playbook object_replication.yml -e "env=<enviorement_name>" --ask-vault-pass
   ```
Enter Ansible-Vault password when prompted.
