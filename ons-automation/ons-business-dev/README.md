# Overview

The purpose of this project is to provide local development environment with the following tools installed:

- Apache Hadoop
- Apache Spark
- Apache Cassandra

# Requirements

## Hardware

Currently virtual machine is configured to use 2 CPU cores and 6 GB of memory.

# What's inside the box

## Installation location

Tools are installed in `/opt` directory. Configuration files are available inside installation directories.

## System services

Following services are available and will start automatically at the boot time:

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

