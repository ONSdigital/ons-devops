# Elasticsearch Role Overview

## Introduction

The `elasticsearch` role is used to setup cluster environment for elasticsearch by provisioning separate data, master and client nodes.
Elasticsearch cluster comprise of the following 3 types of nodes:

- Data node: Physically house the Shards and Data.
- Master node: In-charge of maintaining the cluster state.
- Client node: Handles all query requests and directs them to data nodes. These are important for the overall performance of the cluster


## Requirements

Following steps are required for provisioning elasticsearch cluster.

### Nodes yaml configuration

As the first step we need to define following entry in [nodes.yml](nodes.yml) file depending on the type of node we want to provision:

```
ons-esmaster:
  box: geerlingguy/centos7
  server:
    hostname: ons-esmaster
    memory: 1024
    vcpu: 1
    ip: <IP Address>
  provisioning:
    role: elasticsearch
    environment: development
```
NOTE: The first master node should be provisioned with IP address. This is important for vagrant as there is no DNS service. 
Subsequent master nodes can be provisioned without IP address. FIrst master node is already defined in nodes.yml.

The above will provision elasticsearch master node. Similarly `ons-esdata` and `ons-esclient` nodes are provisioned. 
See [nodes.yml](nodes.yml) file for details on each.

### Ansible playbook

Make sure that the playbook.yml file is defined for the elasticsearch role under `ons-automation/elasticsearch/playbook.yml` folder. 
Sample configuration for `playbook.yml`:

```
---
- hosts: < hostname or hostgroup >
  gather_facts: yes

  roles:
  - geerlingguy.java
  - geerlingguy.elasticsearch
  - elasticcluster
```

The above role will install/configure Java and elasticsearch cluster.

### Inventory configuration

Next step is to update inventory file for development environment whic is setup under `ons-automation/development/inventory_dev`. 
The following configuration, groups the individual servers to the type of node in elasticsearch cluster.

```
[es-masterservers]
ons-esmaster
```
```
[es-clientservers]
ons-esclient
```
```
[es-dataservers]
ons-esdata
```

The above entries will be used to differentiate configurations between the three types of nodes.

At this point the elaticsearch is ready to be provisioned by `vagrant up < nodename >` command.

### Elasticsearch yaml configuration

Elasticsearch nodes will be cnfigured according to the group variables defined in inventory hierarchy structure e.g. `ons-automation/development/group_vars/all`.

```
ons-automation
│   ├── development
│   │   ├── group_vars
│   │   │   ├── all
│   │   │   ├── es-clientservers.yml
│   │   │   ├── es-dataservers.yml
│   │   │   └── es-masterservers.yml
│   │   ├── host_vars
│   │   └── inventory_dev
```

- all: Contains all the common parameters defined for every node in elasticsearch cluster.
- es-clientservers.yml: Contains parameters defined for client servers.
- es-dataservers.yml: Contains parameters defined for data servers.
- es-masterservers.yml: Contains parameters defined for master servers.


