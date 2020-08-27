Rancher Kubernetes Engine(rke) pre-config and deployment
=========

Ansible playbook and roles for Rancher Kubernetes Engine pre-config and deployment.

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

Role Variables
--------------

Role variables are available in `group_vars` directory.

Variables applicable for all the roles are stored in `group_vars/all.yml`.
   ```
    rke_ssh_user: centos
    rke_release: v1.1.4
    kubernetes_version: "1.18"
    ntp_enabled: true
    ntp_timezone: America/New_York
```
Set the required values of these variables before running playbook.

`hosts.ini` file containing the host inventory details, Update this file with host details.

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
        roles:
          - { role: nginx, become: yes }
          - rke-setup

To execute playbook, issue the following command:
( Replace `<ssh_user>` with host ssh user name and `<key_file_path>` with host private key file path )
   ```bash
   $ ansible-playbook rancher_k8s_preconfig.yml -i hosts.ini --user=<ssh_user> --key-file=<key_file_path>
   ```
