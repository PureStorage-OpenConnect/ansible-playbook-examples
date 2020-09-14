Rancher Kubernetes Engine(rke) pre-config and deployment
=========

Ansible playbook and roles to deploy Rancher Kubernetes Engine( rke ).
This role and playbook can be used to deploy rke on CentOS and Ubuntu cloud instances or bare metal nodes.

Disclaimer
------------

##### These sample playbooks and roles not supported by PureStorage.

Requirements
------------

* Install python-pip on Ansible control node.

  CentOS:
    ```bash
    $ sudo yum install epel-release
    $ sudo yum install python-pip
    $ sudo pip install --upgrade pip
    $ pip install ansible
    ```
  Ubuntu:
    ```bash
    $ sudo apt install python-pip
    $ pip install ansible
    ```
  MacOS:
    ```bash
    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $ python get-pip.py --user
    $ pip install --user ansible
    ```
  For more details to install Ansible on MacOS, follow this [link](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-with-pip).

* Install kubernetes collection
  
  ```
  $ ansible-galaxy collection install community.kubernetes
  ```


Role Variables
--------------

Role variables are available in `group_vars` directory.

Variables applicable for all the roles are stored in `group_vars/all.yml`.
   ```
    rke_ssh_user: rke
    rke_release: v1.1.4
    kubernetes_version: "1.18"
    ntp_enabled: true
    ntp_timezone: America/New_York

    # supported docker versions [17.03, 18.06, 18.09.2, 19.03]
    docker_version: 19.03
   ```
Set the required values of these variables before running playbook.

To set loadbalancer dns address, update `loadbalancer_public_dns: ''` with dns address in `group_vars/loadbalancer.yml`. If load balancer dns is not provided, Playbook use the pulic dns address of the `ec2-rke-local-1` node and user can use that to access rancher. In case of bare metal, dns address is `<rke-local-1_ip>.xip.io` if it is not set in varibales. 

`hosts.ini` file containing the host inventory details, Update this file with host details.
As a best practice, we recommend having a minimum of three nodes (VMs or bare-metal) for creating the Rancher management cluster. 

In addition to the three nodes for Rancher management cluster, you need another node to configure the external Load-Balancer like nginx and install Rancher and rke binaries.
Example `hosts.ini` for ec2 instances:
   ```
    [all]
    ec2-rke-local-1     ansible_host=18.237.165.97   private_ip=172.31.15.240 
    ec2-rancher-local-1 ansible_host=34.220.133.148  private_ip=172.31.2.10
    ec2-rancher-local-2 ansible_host=34.220.127.101  private_ip=172.31.0.120
    ec2-rancher-local-3 ansible_host=34.215.63.82    private_ip=172.31.7.212

    [node]
    ec2-rancher-local-1
    ec2-rancher-local-2
    ec2-rancher-local-3

    [loadbalancer]
    ec2-rke-local-1
  ```
Example `hosts.ini` for bare metal :
   ```
    [all]
    rke-local-1     ansible_host=18.237.165.97
    rancher-local-1 ansible_host=34.220.133.148
    rancher-local-2 ansible_host=34.220.127.101
    rancher-local-3 ansible_host=34.215.63.82

    [node]
    rancher-local-1
    rancher-local-2
    rancher-local-3

    [loadbalancer]
    rke-local-1
  ```


This playbook will deploy RKE, Helm 3, kubectl and Rancher.

To access Rancher UI, use Load Balancer public DNS address. 

Note: User can use below pulic AMI's to deploy instances on AWS. 
      CentOS-7: ami-0bc06212a56393ee1
      Ubuntu-18.04: ami-0d1cd67c26f5fca19

Dependencies
------------

None

Example Playbook
----------------

      ---
      - name: Setup ntp and firewall
        hosts: all
        become: true
        roles:
          - ntp
          - firewall

      - name: Setup rke pre-configuration
        hosts: all
        become: true
        roles:
          - rke-preconfig

      - name: Deploy loadbalancer and rke-setup
        hosts: loadbalancer
        become: true
        roles:
          - nginx
          - rke-setup


To execute playbook, issue the following command:
( Replace `<ssh_user>` with host ssh user name and `<key_file_path>` with host private key file path )
   ```bash
   $ ansible-playbook rancher.yml -i hosts.ini --user=<ssh_user> --key-file=<key_file_path>
   ```

To execute playbook with host password instead of private key( Not recommended ), use following command.

   ```bash
   $ ansible-playbook rancher.yml -i hosts.ini -u <ssh_user> -k -K
   ```
Enter remote host password and root password when prompted.