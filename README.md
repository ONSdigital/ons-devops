# Overview

This purpose of this vagrant project is to provide local development environment for Registers project with following tools installed:

- Apache Hadoop
- Apache Spark
- Apache Cassandra

This will also serve the installation of elasticsearch (Data,Master and CLient nodes) to test the elasticsearch configuration and automation using Ansible.

# Requirements

## Hardware

The use of CPU and RAM is configurable via nodes.yaml configuration file. e.g.

ons-business-dev:
  hostname: ons-business-dev
  memory: 4096
  vcpu: 2
  role: ons-business-dev
  environment: vagrant

## Software

Beside hardware requirement the following tools have to be installed on the host machine prior to provisioning development environment:

- VirtualBox (https://www.virtualbox.org)
- Vagrant (https://www.vagrantup.com)

Note: It is recommended to use latest version of Vagrant (1.8.4) as earlier versions had issues with Ansible 2.0 (https://www.ansible.com).

# How to use it

## Provisioning environment for the first time

To provision development environment from scratch please execute following command from project root directory:

```
vagrant up ons-business-dev
```
To spin up elasticsearch data node

```
vagrant up es-data
```

Above command will download latest CentOS 7 image (https://atlas.hashicorp.com/centos/boxes/7) and provision environment using `ons-automation/ons-business-dev.yml` playbook.
The usage of the box is also configurable in Vagrantfile via 
config.vm.box = "geerlingguy/centos7" or config.vm.box = "centos/7"

## Provisioning environment later on

Provisioning can be executed at any time using following command from project root directory:

```
vagrant rsync && vagrant provision
```

# How to get inside the box

To get inside the box execute following command from project root directory.

```
vagrant ssh ons-business-dev
```

Above command will log you in as a default `vagrant` user. To acquire root access execute following command (no password required):

```
sudo -i
```

# What's inside the box

## Installation location

Tools are installed in `/opt` directory. Configuration files are available inside installation directories.

## System services

Following services are available and will start automatically at boot time:

- dfs-name-node
- dfs-data-node
- yarn-resource-manager
- yarn-node-manager
- apache-cassandra

To manage above services use `service` command, for example:

```
service dfs-name-node restart
```

## HDFS configuration

HDFS is configured to store 1 replica of data under `/var/local/hadoop/dfs` directory.
