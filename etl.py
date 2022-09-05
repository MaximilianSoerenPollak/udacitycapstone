import configparser
import psycopg2

from sys import argv
from s3_to_redshift import create_tables, insert_data, drop_tables

# --- CONFIG ----
config = configparser.ConfigParser()
config.read_file(open("dwh.cfg"))

DWH_CLUSTER_IDENTIFIER = config.get("CLUSTER", "DWH_CLUSTER_IDENTIFIER")
DWH_DB = config.get("CLUSTER", "DB_NAME")
DWH_DB_USER = config.get("CLUSTER", "DB_USER")
DWH_DB_PASSWORD = config.get("CLUSTER", "DB_PASSWORD")
DWH_PORT = config.get("CLUSTER", "DB_PORT")
DWH_ENDPOINT = config.get("CLUSTER", "DWH_ENDPOINT")


def drop_tables_function(cur, conn):
    for query in drop_tables:
        cur.execute(query)
        conn.commit()


def create_tables_function(cur, conn):
    for query in create_tables:
        cur.execute(query)
        conn.commit()


def load_data(cur, conn):
    for query in insert_data:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read("dwh.cfg")

    conn_string = "postgresql://{}:{}@{}:{}/{}".format(
        DWH_DB_USER, DWH_DB_PASSWORD, DWH_ENDPOINT, DWH_PORT, DWH_DB
    )
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    # Asking the user if he wants to drop the tables.
    if argv[1].lower() == "y":
        drop_tables_function(cur, conn)
    # Always executed since ("If exists") decleration in SQL.
    create_tables_function(cur, conn)
    # Asking the user if he wants to load the data.
    if argv[2].lower() == "y":
        load_data(cur, conn)
    conn.close()


if __name__ == "__main__":
    main()
