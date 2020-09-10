Install OS packages
=========

Ansible playbook and role to install pyhton3, nfs-utils and pip3 OS packages along with python modules boto3 and numpy on Ubuntu and CentOS.


Requirements
------------

* Setup Ansible control node to execute this playbook

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
  MacOS
    ```bash
    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $ python get-pip.py --user
    $ pip install --user ansible
    ```
  For more details to install Ansible on MacOS, follow this [link](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-with-pip).

Role Variables
--------------

Role variables are available in `roles/common_packages/defaults/main.yml` directory.
   ```
    ubuntu_packages:
        - python3
        - python3-pip
        - nfs-common

    centos_packages:
        - python3
        - python3-pip
        - nfs-utils

    pip_install_packages:
        - boto3
        - numpy
```

Set the required values for these variables before running playbook.

`hosts.ini` file containing the host inventory details, Update this file with host details.

Dependencies
------------

None

Example Playbook
----------------

    ---
    - name: Install common packages
      hosts: all
      become: true
      roles:
        - common_packages

To execute playbook, issue the following command:
( Replace `<ssh_user>` with host ssh user name and `<key_file_path>` with host private key file path )
   ```bash
   $ ansible-playbook install_common_packages.yml -i hosts.ini -u <ssh_user> --key-file=<key_file_path>
   ```

To execute playbook with host password instead of private key( Not recommended ), use following command.

   ```bash
   $ ansible-playbook install_common_packages.yml -i hosts.ini -u <ssh_user> -k -K
   ```
Enter remote host password and root password when prompted.