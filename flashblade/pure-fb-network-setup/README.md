FlashBlade Network setup
=========

Ansible playbook and role to setup FlashBlade Network.

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

There are two variable files "fb_details.yml" and "fb_secrets.yml" are holding the Ansible variables for the role at path `vars/<enviorement_name>`. 

This role and playbook can be used to setup network on FlashBlade servers in different environments. To store role variable files, User can create different directories with `vars/<environment_name>`. User must specify `<environment_name>` while running `ansible-playbook` by specifying value in extra vars command line flag `-e "env=<environment_name>"`.

Ansible playbooks require API token to connect to FlashBlade servers. API token can be obtained by connecting FlashBlade management VIP through ssh for a specific user and running the following purity command.
   ```
   $ ssh <pureuser>@<pure_fb_mgmt_ip>
   $ pureadmin list <username> --api-token -–expose
   ```
Update "api_token" obtained from FlashBlade in "fb_secrets.yml" file and "fb_url" value with FlashBlade Management VIP in "fb_details.yml".

Encrypt "fb_secrets.yml" using Ansible-Vault and enter password when prompted. This password is required to run playbook.
```
$ ansible-vault encrypt fb_secrets.yml
```

Update variables in `fb_details.yml` and `fb_secrets.yml` files to the desired values.

* fb_details.yml
   ```
   # FBServer details
    array_inventory:               
      FBServer1:
        fb_url: 10.xx.126.80
        network:
            dns: 
              - { domain: "purelab.purestorage.com", nameservers: [10.12.133.15, 10.12.133.16] } 
            ntp: 
              - { servers: [10.22.93.14, 10.21.86.15] }   
            ds:                           
              - { dstype: nfs, enable: true, uri: "ldaps://lab.purestorage.com", base_dn: "DC=lab,DC=purestorage,DC=com", bind_user: Administrator, bind_password: password } 
              - { dstype: smb, enable: true, uri: "ldaps://lab.purestorage.com", base_dn: "DC=lab,DC=purestorage,DC=com", bind_user: Administrator, bind_password: password } 
              - { dstype: management, enable: true, uri: "ldaps://lab.purestorage.com", base_dn: "DC=lab,DC=purestorage,DC=com", bind_user: Administrator, bind_password: password }   
            subnet: 
              - { name: VLAN2250, prefix: "10.21.250.0/24", vlan: 2250, gateway: 10.21.250.1, mtu: 1500 }
              - { name: VLAN2210, prefix: "10.21.210.0/24", vlan: 2210, gateway: 10.21.210.1 } # default mtu: 1500
            vip: 
              - { name: datavip1-2250, address: 10.21.250.7 } # deafault services: data
              - { name: replvip1-2210, address: 10.21.210.22, services: replication }                               
    ```

* fb_secrets.yml
    ```
    array_secrets:               
      FBServer1:
        api_token: T-c61e4dec-xxxx-4264-87f8-315264d9e65a
    ```
#### Note
 * Default `mtu` value is 1500 in subnet configuration. User can set desired "mtu" value in fb_details.yml file.
 * Only one replication interface(VIP) is allowed on FlashBlade server. If user try to create multiple replication VIP through Ansible playbook, There will be an error `Interface creation failed`.
 * To delete any of the network configuration use `state: disabled` in `fb_details.yml` variable file. When playbook executed with below variables in `fb_details.yml`, It will delete data VIP `datavip1-2250` and replication VIP `replvip1-2210`.
     ```
   # FBServer details
    array_inventory:               
      FBServer1:
        fb_url: 10.xx.126.80
        network:
          vip: 
            - { name: datavip1-2250, state: disabled }
            - { name: replvip1-2210, state: disabled }                               
    ```
 * To extend the network setup configuration on the fleet of FlashBlade Arrays, add multiple "FBServer1...N" blocks under array_inventory in "fb_details.yml" file.
 Example configuration to setup DNS on two FlashBlade servers.
   
   **fb_details.yml**
   ```
   # FBServer details
    array_inventory:               
      FBServer1:
        fb_url: 10.xx.126.80
        network:
          dns: 
            - { domain: "purelab.purestorage.com", nameservers: [10.12.133.15, 10.12.133.16] } 
      FBServer2:
        fb_url: 10.xx.126.110
        network:
          dns: 
            - { domain: "purelab1.purestorage.com", nameservers: [10.12.132.11, 10.12.132.14] } 
    ```
    **fb_secrets.yml**
    
    ```
    array_secrets:               
      FBServer1:
        api_token: T-c61e4dec-xxxx-4264-87f8-315264d9e65a
      FBServer2:
        api_token: T-d88e4dec-xxxx-4222-87g3-315264d9e77a
    ```
Dependencies
------------

None

Example Playbook
----------------

      - name: FlashBlade Network setup
        hosts: localhost
        gather_facts: false
        vars_files:
        - "vars/{{ env }}/fb_details.yml"
        - "vars/{{ env }}/fb_secrets.yml"
        roles:
            - purefb_network_setup

To execute playbook, issue the following command:
( Replace `<enviorement_name>` with the correct value )
   ```bash
   $ ansible-playbook purefb_network_setup.yml -e "env=<enviorement_name>" --ask-vault-pass
   ```
Enter Ansible-Vault password which used to encrypt "fb_secrets.yml" file.
