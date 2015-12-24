#!/usr/bin/python
import psycopg2, json, os
from sys import argv
from apiwall.blockchainrpc import RPC
from apiwall.settings import Config

name, txid = argv

def main():
    #Define our connection string
    conn_string = "host='localhost' dbname='{0}' user='{1}' password='{2}'".format(Config.SQLALCHEMY_DATABASE_URI.split("///")[1], Config.APIWALL_DB_USER, Config.APIWALL_DB_USER_PASSWORD)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

    rpc = RPC(url="http://{0}:{1}@localhost:{2}".format(Config.RPC_USER, Config.RPC_PASSWORD, Config.RPC_PORT))

    tx_json = rpc.call("gettransaction", txid)

    #We want to check and see if the transaction already exists in the DB before inserting
    cursor.execute("""SELECT * from BLOCKCHAIN_TRANSACTIONS WHERE blkchtx_id = '{0}'""".format(txid))

    rows = cursor.fetchall()

    if len(rows) > 0:
        return

    address = tx_json.get("details")[0].get("address")

    cursor.execute("""SELECT * from invoices WHERE payment_address = '{0}'""".format(address))

    rows = cursor.fetchall()

    #Insert new transaction
    cursor.execute("INSERT INTO BLOCKCHAIN_TRANSACTIONS (BLKCHTX_JSON, INVOICE_ID, BLKCHTX_ID) VALUES ('{0}', '{1}', '{2}')".format(json.dumps(tx_json), rows[0][0], txid));

    conn.commit()

if __name__ == "__main__":
    main()

