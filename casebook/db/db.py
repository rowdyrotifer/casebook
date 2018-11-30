import argparse
import configparser
import os

import bcrypt
import mysql.connector

database_config = configparser.ConfigParser('')
database_config.read(os.path.join(os.path.dirname(__file__), 'database.ini'))


def get_full_db_connection():
    conn = get_db_connection()
    conn.database = database_config['MySQL']['database']
    return conn


def get_db_connection():
    return mysql.connector.connect(
        host=database_config['MySQL']['host'],
        user=database_config['MySQL']['user'],
        passwd=database_config['MySQL']['password']
    )


def do_delete():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS `{database_config['MySQL']['database']}`")
    conn.commit()


def do_init():
    dbname = database_config['MySQL']['database']

    conn = get_db_connection()

    print(f"Creating database `{dbname}`")
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET = `utf8` COLLATE `utf8_general_ci`")
    conn.commit()

    print(f"Selecting database `{dbname}`.")
    conn.database = dbname

    print("Creating `users` table...")
    # password is bcrypt format
    mk_users = """CREATE TABLE IF NOT EXISTS `users` (
              `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
              `username` VARCHAR(64) UNIQUE NOT NULL,
              `password` BINARY (60) NOT NULL
            );"""
    cursor.execute(mk_users)

    print("Creating `session` table...")
    mk_session = """CREATE TABLE IF NOT EXISTS `session` (
                  `token` VARCHAR(32) PRIMARY KEY NOT NULL,
                  `user_id` INT NOT NULL,
                  `expiration_time` DATETIME NOT NULL,
                  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );"""
    cursor.execute(mk_session)

    print("Creating `post` table...")
    mk_post = """CREATE TABLE IF NOT EXISTS `post` (
                  `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                  `author_id` INT NOT NULL,
                  `posted_time` TIMESTAMP NOT NULL,
                  `title` TEXT NOT NULL,
                  `body` MEDIUMTEXT NOT NULL,
                  FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
                );"""
    cursor.execute(mk_post)

    print("Creating `follow` table...")
    mk_follow = """CREATE TABLE IF NOT EXISTS `follow` (
                      `following_id` INT NOT NULL,
                      `follower_id` INT NOT NULL,
                      PRIMARY KEY (following_id, follower_id),
                      FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
                      FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE
                    );"""
    cursor.execute(mk_follow)


def do_fill_users(conn):
    cursor = conn.cursor()
    users = [
        (1, 'mark',  'mark',  b'$2b$12$II5aKVfQ0lqNEXhoB4I84u'),
        (2, 'brian', 'brian', b'$2b$12$vn3oQ/ap/4snuzcSqAuf1O'),
        (3, 'david', 'david', b'$2b$12$vpikI1Gsn.bisYBsT7zfH.'),
        (4, 'jason', 'jason', b'$2b$12$futEJBBDdf50MNKugTATYe')
    ]
    buffer = []
    for id, username, password, salt in users:
        buffer.append((id, username, bcrypt.hashpw(password.encode('utf8'), salt)))
    cursor.executemany("INSERT INTO users(id, username, password) VALUES (%s, %s, %s)", buffer)
    conn.commit()


def do_fill_post(conn):
    cursor = conn.cursor()
    # In app using datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    buffer = [
        (1, 1, '2018-11-29 21:53:42', 'My mother just died.', 'Please don\'t ask me how.'),
        (2, 1, '2018-11-29 22:53:42', 'Hello there world.', 'It\'s a whole new day.'),
        (3, 2, '2018-11-24 10:51:42', 'My name is Brian1.', 'My name is Brian1 and I am a student at BrianU.'),
        (3, 2, '2018-11-24 10:51:42', 'My name is Brian2.', 'My name is Brian2 and I am a student at BrianU.'),
        (3, 2, '2018-11-24 10:51:42', 'My name is Brian3.', 'My name is Brian3 and I am a student at BrianU.')
    ]
    cursor.executemany("INSERT INTO post(id, author_id, posted_time, title, body) VALUES (%s, %s, %s, %s, %s)", buffer)
    conn.commit()


def do_fill_follow(conn):
    cursor = conn.cursor()
    pairs = [
        (1,3),
        (2,3),
        (4,3),
        (2,4),
        (4,2),
        (3,4)
    ]
    cursor.executemany("insert into follow (following_id, follower_id) values (%s, %s)", pairs)
    conn.commit()


def do_fill():
    conn = get_db_connection()
    conn.database = database_config['MySQL']['database']
    do_fill_users(conn)
    do_fill_post(conn)
    do_fill_follow(conn)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform some primitive database operations')
    parser.add_argument('actions', nargs='+', choices={'delete', 'init', 'fill'}, help='actions to perform')
    for action in parser.parse_args().actions:
        print(f'Running {action} action:')
        method_to_call = globals()[f'do_{action}']()
        print(f'Finished {action} action!')
        print()
