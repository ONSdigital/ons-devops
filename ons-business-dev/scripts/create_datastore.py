#!/usr/bin/env python

import logging

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

from cassandra.cluster import Cluster

KEYSPACE = "bi"
BUSINESSINDEX_TABLE = "businessindex_by_matchkey"
STARTED_EXTRACTS_TABLE = "started_extracts"

# Host IP of the Cassandra instance or cluster
CLUSTER_IP = "localhost"

def main():
    cluster = Cluster([CLUSTER_IP])
    session = cluster.connect()
    meta = cluster.metadata

    if KEYSPACE in meta.keyspaces:
        log.info("dropping existing keyspace...")
        session.execute("DROP KEYSPACE " + KEYSPACE)

    log.info("creating keyspace: " + KEYSPACE)
    session.execute("""
        CREATE KEYSPACE %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
        """ % KEYSPACE)

    log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)

    create_business_table(session)
    create_started_extracts_table(session)

    session.shutdown()
    cluster.shutdown()
    log.info("Connection closed...")


def create_business_table(session):
    log.info("creating table" + BUSINESSINDEX_TABLE)
    session.execute("""
            CREATE TABLE %s (
                business_id text,
                match_key text,
                data_source text,
                business_name text,
                postcode text,
                industry_code text,
                legal_status text,
                trading_status text,
                turnover decimal,
                total_employees int,
                PRIMARY KEY(match_key, business_name, postcode, business_id, data_source)
            );
            """ % BUSINESSINDEX_TABLE)


def create_started_extracts_table(session):
    log.info("creating table" + STARTED_EXTRACTS_TABLE)
    session.execute("""
        CREATE TABLE %s (
            extract_id text,
            summary_only boolean,
            PRIMARY KEY(extract_id)
        );
        """ % STARTED_EXTRACTS_TABLE)


if __name__ == "__main__":
    main()
