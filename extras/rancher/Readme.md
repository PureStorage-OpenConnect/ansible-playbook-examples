Rancher Kubernetes Engine(rke) pre-config and deployment
=========

Ansible playbook and roles to deploy Rancher Kubernetes Engine( rke ).

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
    docker_version: 18.09.2
   ```
Set the required values of these variables before running playbook.

`hosts.ini` file containing the host inventory details, Update this file with host details.
As a best practice, we recommend having a minimum of three nodes (VMs or bare-metal) for creating the Rancher management cluster. 

In addition to the three nodes for Rancher management cluster, you need another node to configure the external Load-Balancer like nginx and install Rancher and rke binaries.
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

This playbook will deploy RKE, Helm 3, kubectl and Rancher.

To access Rancher UI, use Load Balancer public DNS address. 

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
