import argparse
import configparser
import os

import mysql.connector


def do_delete():
    pass


database_config = configparser.ConfigParser('')
database_config.read(os.path.join(os.path.dirname(__file__), 'database.ini'))


def get_db_connection():
    return mysql.connector.connect(
        host=database_config['MySQL']['host'],
        user=database_config['MySQL']['user'],
        passwd=database_config['MySQL']['password']
    )


def do_init():
    dbname = database_config['MySQL']['database']

    conn = get_db_connection()

    print(f"Creating database {dbname}")
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET = `utf8` COLLATE `utf8_general_ci`")
    conn.commit()

    print(f"Selecting database {dbname}.")
    conn.database = dbname

    print("Creating `user` table...")
    # password is bcrypt format
    mk_user = """CREATE TABLE IF NOT EXISTS `user` (
              `username` VARCHAR(64) PRIMARY KEY NOT NULL,
              `password` BINARY (60) NOT NULL
            );"""
    cursor.execute(mk_user)

    print("Creating `user` table...")
    # password is bcrypt format
    mk_user = """CREATE TABLE IF NOT EXISTS `user` (
              `username` VARCHAR(64) PRIMARY KEY NOT NULL,
              `password` BINARY (60) NOT NULL
            );"""
    cursor.execute(mk_user)


def do_fill():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform some primitive database operations')
    parser.add_argument('actions', nargs='+', choices={'delete', 'init', 'fill'}, help='actions to perform')
    for action in parser.parse_args().actions:
        method_to_call = globals()[f'do_{action}']()
