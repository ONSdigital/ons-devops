# ONS-Registers Vagrant Environment Setup

The purpose of this project is to provide the capability to provision vagrant hosted environments (e.g development) for ONS Registers project. 
ONS Registers project comprises of 2 separate streams:

- Address Index
- Business Index

This Vagrant provisioning will cater both the needs.

# Pre-requisites

- Vagrant (https://www.vagrantup.com/downloads.html)
- Virtualbox (https://www.virtualbox.org/wiki/Downloads)

Note: It is recommended to use latest version of Vagrant i.e. >= 1.8.4, as earlier versions had issues with Ansible 2.0.

# Important files:

 - nodes.yml: The file contains all the details of the nodes which you can provision via vagrant up < nodename > command. For more details see the comments in the file https://github.com/ONSdigital/ons-devops/blob/ons-devops-new/nodes.yaml .
 - ons-automation/development/inventory_dev: The file contains the information about the groups of inventories in Ansible. This will be used to separate the variables for different environments and groups of hosts.

# ONS Business Index environment
----------------------------------

ONS Business Index development environment includes following tools to be setup:

- Apache Hadoop  (http://hadoop.apache.org/)
- Apache Spark  (http://spark.apache.org/)
- Apache Cassandra  (http://cassandra.apache.org/)

## Hardware Requirements
Installing the above tools can be resource heavy. A typical setup requires, 4GB of RAM and 2 Cores CPU. For the sake of simplicity the CPU and RAM
is made configurable via nodes.yaml file and can be modified as below:

```
ons-business-dev:
  box: geerlingguy/centos7
  server:
    hostname: ons-business-dev
    memory: 6144
    vcpu: 2
  provisioning:
    role: ons-business-dev
    environment: vagrant
```

NOTE: In the above configuration ROLE is very important as this will decide which ansible playbook to execute. It should not be modified unless a custom 
playbook with the same name has been provided. Following roles can be provided to a vagrant box:

- ons-business-dev     (ONS Business Index development environment)
- es-standalone        (Elasticsearch standalone installation) 
- data                 (Elasticsearch Data node)
- client               (Elasticsearch client node)
- master               (Elasticsearch master node)

## Usage example

## Provisioning environment for the first time

Start the development VM (creating it if necessary):

```
$ vagrant up ons-business-dev
```

## Log in to the development VM

```
$ vagrant ssh ons-business-dev
```

Above command will use the default 'vagrant' user to log in. In order to acquire root access execute any of the commmands below (no password required):

```
sudo -i
```

or 

```
sudo su
```

## Update and apply the ansible code to the development vagrant box e.g. ons-business-dev

```
vagrant provision ons-business-dev
```

## What's inside the box

## Installation location

Tools are installed in `/opt` directory.

## System services

Following services are available and will start automatically at boot time:

- dfs-name-node
- dfs-data-node
- yarn-resource-manager
- yarn-node-manager
- apache-cassandra

To manage above services use `service` or 'systemctl' command, for example:

```
service dfs-name-node restart
```

or

```
systemctl restart dfs-name-node
```

## HDFS configuration

HDFS is configured to store 1 replica of data under `/var/local/hadoop/dfs` directory.
