# ONS-Registers Vagrant Environments

The project models local vagrant hosted equivalents of the ONS environments. It caters for both the streams:

- Address Index
- Business Index

## Pre-requisites

- [Vagrant](https://www.vagrantup.com/downloads.html)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Git](https://git-scm.com/downloads)

Note: It is recommended to use latest version of Vagrant i.e. >= 1.8.4, as earlier versions had issues with Ansible 2.0.

## Nodes
 - [nodes.yml] (nodes.yml): The file contains the details of the virtual machines that can be provisioned via this project.
The format of the file is shown below:

```
< nodename >:
  box: < boxname >
  server:
    hostname: < hostname of the box >
    memory: < amount of memory allocated to the VM >
    vcpu: < virtual CPU allocated to the VM >
    ip: < IP address can be provided if it is needed >
  provisioning:
    role: < Role that is served by the VM >
    environment: < environment that is being created >
```

## Roles

Roles define the configuration of the virtual machine being provisioned.
At the moment following roles can be given to a vagrant box:

- [ons-business-dev](ons-automation/ons-business-dev): (ONS Business Index development environment)
- [elasticsearch](ons-automation/elasticsearch): (Elasticsearch standalone installation)
- [es-standalone](ons-automation/es-standalone): (Elasticsearch cluster provisioning)

## Environments and Configurations

### Inventory

The inventory file located in `ons-automation/development/inventory_dev` (this is the inventory file for development environment only) 
contains the host entries and their groups. e.g.

```
[es-masterservers]
ons-esmaster ansible_connection=local
```

This is the standard group format from ansible. This ensures that `ons-esmaster` node belongs to the list `es-masterservers` group. 
The groups are created to ensure same configuration across the similar set of nodes. More about ansible inventories [here](http://docs.ansible.com/ansible/intro_inventory.html). The inventory structure followed currently is shown below:

```
├── ons-automation
│   ├── development
│   │   ├── group_vars
│   │   │   ├── all
│   │   │   ├── es-clientservers.yml
│   │   │   ├── es-dataservers.yml
│   │   │   └── es-masterservers.yml
│   │   ├── host_vars
│   │   └── inventory_dev
```

NOTE: Make sure the nodenames are same across the nodes.yml and inventory file.

## Vagrant Usage example

Start the development VM (creating it if necessary):
```
$ vagrant up < nodename >
```

Log in to the development VM
```
$ vagrant ssh < nodename >
```

Above command will use the default 'vagrant' user to log in. In order to acquire root access execute any of the commmands below (no password required):

```
sudo -i
```
or 
```
sudo su
```

Update and apply the ansible code to the development vagrant box.
```
vagrant provision < nodename >
```

Stop all VMs
```
vagrant halt
```
or to stop specific VM
```
vagrant halt < nodename >
```

Delete all VMs
```
vagrant destroy
```
or to destroy specific VM
```
vagrant destroy < nodename >
```

## Details

The [Ansible](https://www.ansible.com/) environment is prepared during provisioning for use in the guest VM.

On the Vagrant hosts:

- The `ons-automation/roles` will be cloned from either [Ansible Galaxy](https://galaxy.ansible.com/intro) or from the ONS github.
- The `ons-automation/#{environment}/` will be cloned from github. This will be used for configuration of the guest VM.

In the guest VM:

- Ansible will be installed.

Ansible is then invoked with the playbook path set to `ons-automation/#{cfgOptions['provisioning']['role']}/playbook.yml'.

The dedicated playbook for each of the roles in the [Roles](##Roles) section has seprate README files to describe its details.

- [ons-business-dev](ons-automation/ons-business-dev)
- [elasticsearch](ons-automation/elasticsearch)
- [es-standalone](ons-automation/es-standalone)
