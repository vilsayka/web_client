import psycopg2
from config import DATABASE_URL_MASTER, DATABASE_URL_SLAVE


def get_master_connection():
    return psycopg2.connect(DATABASE_URL_MASTER)


def get_slave_connection():
    return psycopg2.connect(DATABASE_URL_SLAVE)