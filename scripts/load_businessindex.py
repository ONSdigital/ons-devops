#!/usr/bin/env python

import argparse
import logging
import math

from decimal import Decimal
from decimal import InvalidOperation

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

import csv
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra.query import BatchStatement

KEYSPACE = "bi"
BUSINESSINDEX_TABLE = "businessindex_by_matchkey"

# Fieldnames to insert into in the Cassandra businessindex table
FIELDNAMES = "match_key, business_id, data_source, business_name, postcode, " \
             "industry_code, legal_status, trading_status, turnover, total_employees"

# Replacments corresponding to each of the fieldnames in the table
# These correspond to the dictionary read in from the csv header
REPLACEMENTS = "%(MATCH_KEY)s, %(BUSINESS_ID)s, %(DATA_SOURCE)s, %(BUSINESS_NAME)s, %(POSTCODE)s, " \
             "%(INDUSTRY_CODE)s, %(LEGAL_STATUS)s, %(TRADING_STATUS)s, %(TURNOVER)s, %(TOTAL_EMPLOYEES)s"

# Host IP of the Cassandra instance or cluster
CLUSTER_IP = "localhost"

# Batch size to split insert into:
BATCH_SIZE = 200


def setup_session(cluster_ip, keyspace):
    cluster = Cluster([cluster_ip])
    session = cluster.connect()

    log.info("setting keyspace...")
    session.set_keyspace(keyspace)
    return session


def close_session(session):
    session.shutdown()
    log.info("Connection closed...")


def load_businessindex(session, csv_path):
    log.info("Opening " + csv_path)

    # get the number of lines
    with open(csv_path, 'rb') as csvlines:
        line_count = sum(1 for line in csvlines) - 1

    number_of_batches = int(math.ceil(Decimal(line_count)/BATCH_SIZE))
    batches_complete = 0

    with open(csv_path, 'rb') as csvfile:

        reader = csv.DictReader(csvfile, skipinitialspace=True)

        query = SimpleStatement("""
            INSERT INTO %s (%s)
            VALUES (%s)
            """ % (BUSINESSINDEX_TABLE, FIELDNAMES, REPLACEMENTS))

        log.info("Query statement:\n%s" % query.query_string)

        batch = BatchStatement()
        for row in reader:
            try:
                row["TURNOVER"] = Decimal(row.get("TURNOVER"))
            except InvalidOperation:
                # TURNOVER is empty
                row["TURNOVER"] = None

            try:
                row["TOTAL_EMPLOYEES"] = int(row.get("TOTAL_EMPLOYEES"))
            except ValueError:
                # TOTAL_EMPLOYEES is empty
                row["TOTAL_EMPLOYEES"] = None

            batch.add(query, row)

            if (reader.line_num - 1) % BATCH_SIZE == 0:
                log.debug("Executing batch %s/%s insert with %s records" % (batches_complete+1, number_of_batches,
                                                                            BATCH_SIZE))
                session.execute(batch)
                batches_complete += 1
                batch = BatchStatement()

        if number_of_batches > batches_complete:
            log.debug("Executing batch %s/%s insert with %s records" % (batches_complete+1, number_of_batches,
                                                                        line_count-(batches_complete*BATCH_SIZE)))
            session.execute(batch)
            batches_complete += 1


def main(path):
    session = setup_session(CLUSTER_IP, KEYSPACE)
    load_businessindex(session, path)
    close_session(session)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="The Business Index extract to load into Cassandra", type=str)
    args = parser.parse_args()

    main(args.input)
