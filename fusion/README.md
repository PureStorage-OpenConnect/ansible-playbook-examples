# Ansible Playbooks for the Fusion DevKit

## Summary
The goal of this document is to help you set up and understand the functionality and scope of the ansible playbooks provided here.


### How run a playbook
```
ansible-playbook playbook_name.yml
```

### Environment Variables
In almost every playbook, there are 2 lines that require an environment variable

```
issuer_id: "{{ ansible_env.FUSION_ISSUER_ID}}"
private_key_file: "{{ ansible_env.FUSION_PRIVATE_KEY_FILE}}"
```
In this case, the variables are: FUSION_ISSUER_ID and FUSION_PRIVATE_KEY_FILE
To set them, you can temporarily enable them with:
```
export FUSION_ISSUER_ID='pure1:apikey:123456789'
export FUSION_PRIVATE_KEY_FILE='/home/user/key.pem'
```
in the case of ```FUSION_PRIVATE_KEY_FILE```, the path to the ```key.pem``` need to be aboslute.

If you prefer to not use environment variables, you can change the values inside the playbook:

```
issuer_id: "<your_API_Application_ID_here>"
private_key_file: "/home/user/key.pem"
```

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
