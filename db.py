import sqlite3
from sqlite3 import Error
import time
import uuid


DB_FILE = 'credit_system.db'


def _create_table(conn, sql):
    if conn is not None:
        try:
            conn.execute(sql)
            conn.commit()
        except Error as e:
            print(e)
    else:
        raise Exception('Failed to create database cursorection')


def connect():
    return sqlite3.connect(DB_FILE)


def init_accounts_table(conn):
    _create_table(conn, ''' CREATE TABLE IF NOT EXISTS accounts (
                                id int PRIMARY KEY,
                                balance integer NOT NULL,
                                max_balance integer NOT NULL,
                                min_balance integer NOT NULL
                        ); ''')


def init_offer_categories_table(conn):
    _create_table(conn, ''' CREATE TABLE IF NOT EXISTS offer_categories(
                                offer_id text,
                                category text,
                                PRIMARY KEY (offer_id, category)
                            ); ''')


def init_offers_table(conn):
    _create_table(conn, ''' CREATE TABLE IF NOT EXISTS offers (
                                id text,
                                seller_id integer,
                                description text NOT NULL,
                                price integer NOT NULL,
                                title text NOT NULL,
                                PRIMARY KEY (id, seller_id),
                                FOREIGN KEY(seller_id) REFERENCES members(id)
                            ); ''')


def init_transactions_table(conn):
    _create_table(conn, ''' CREATE TABLE IF NOT EXISTS transactions (
                                id text PRIMARY KEY,
                                buyer_id int NOT NULL,
                                offer_id text,
                                status text NOT NULL,
                                start_timestamp int NOT NULL,
                                end_timestamp int,
                                FOREIGN KEY(buyer_id) REFERENCES members(id),
                                FOREIGN KEY(offer_id) REFERENCES offers(id)
                            );''')
