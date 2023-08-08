# Ansible Playbooks for the Fusion DevKit

## Prerequisites


### Ansible galaxy

Install Ansible galaxy.

```shell
pip3 install ansible
```


### Ansible Collections

Install required Ansible Collections.

```shell
ansible-galaxy install -r requirements.yml
```


## Summary
The goal of this document is to help you set up and understand the functionality and scope of the ansible playbooks provided here.


### How run a playbook
```
ansible-playbook playbook_name.yml
```

### Authentication

The most common method for authentication is to use an issuer ID and private key file.
This can be set with the `issuer_id` and `private_key_file` parameters:

```
issuer_id: "{{ ansible_env.FUSION_ISSUER_ID}}"
private_key_file: "{{ ansible_env.FUSION_PRIVATE_KEY_FILE}}"
```

In this case, we are using the `FUSION_ISSUER_ID` and `FUSION_PRIVATE_KEY_FILE` environment variables.
You can set them with

```
export FUSION_ISSUER_ID='pure1:apikey:123456789'
export FUSION_PRIVATE_KEY_FILE='/home/user/key.pem'
```

In the case of ```FUSION_PRIVATE_KEY_FILE```, the path to the ```key.pem``` needs to be absolute.

If you prefer to not use environment variables, you can change the values inside the playbook:

```
issuer_id: "<your_API_Issuer_ID_here>"
private_key_file: "/home/user/key.pem"
```

If you are using an encrypted private key, you can use the `private_key_password` field to specify the password for it.

As an alternative form of authentication, you can use the `access_token` field or the `FUSION_ACCESS_TOKEN` env var to provide an API access token directly.

You can change the Fusion API host and token endpoint by specifying `FUSION_API_HOST` and `FUSION_TOKEN_ENDPOINT` env vars respectively.

## Folder: simple
This series of playbooks are meant to run as standalone, so no need for external input, and all information required to create a resource/element are inside each playbook.
Some elements need a previous element to exist to be linked.

## Folder: sample_production
This series of playbooks are meant to run based on the info inside the files in folder ```group_vars```.
Usually the name in the files are almost identical.
To detect without error what files are linked to specific playbook, look inside the same, there will be an import with the value:path to the file.
```
   - ansible.builtin.include_vars: group_vars/consumer.yml
```

### sample_production/inventory.ini
Inside this file, you can declare your hosts that will act as initiators.
```
[Initiators_Hosts]
initiatorserver1
initiatorserver2
initiatorserver3
```
In this example we have declared 3 hosts, and for each one inside folder ```host_vars``` in the current folder, you will find a file ```.yml``` that matches the name of the host initiator.
Inside there is a template that covers the minimal information ansible needs to make the connection with that host.
```
ansible_user: username
ansible_host: 192.168.1.100
ansible_ssh_private_key_file: ~/.ssh/<private_key_file>
```
