# Overview

This purpose of this project is to provide local development environment with following tools installed:

- Apache Hadoop
- Apache Spark
- Apache Cassandra

# Requirements

## Hardware

Currently virtual machine is configured to use 2 CPU cores and 6 GB of memory so these have to be available on the host machine.

## Software

Beside hardware requirement the following tools have to be installed on the host machine prior to provisioning development environment:

- VirtualBox (https://www.virtualbox.org)
- Vagrant (https://www.vagrantup.com)

Note: It is recommended to use latest version of Vagrant as earlier versions didn't work well with Ansible 2.0 (https://www.ansible.com).

# How use it

## Provisioning environment for the first time

To provision development environment from scratch please execute following command from project root directory:

```
vagrant up
```

Above command will download latest CentOS 7 image (https://atlas.hashicorp.com/centos/boxes/7) and provision environment using `provisioning/playbook.yaml` playbook.

## Provisioning environment later on

Provisioning can be executed at any time using following command from project root directory:

```
vagrant rsync && vagrant provision
```

# How to get inside the box

To get inside the box execute following command from project root directory.

```
vagrant ssh
```

Above command will log you in as a default `vagrant` user. To acquire root access execute following command (no password required):

```
sudo -i
```

It is also possible to access a box using `192.168.33.100` IP address (most of the ports are open from outside).

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
