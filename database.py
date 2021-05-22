import sqlite3
from sqlite3 import Error
import pandas as pd
from pandas import DataFrame

DB_NAME = r"D:\Game_Launcher\usersDB.db"


def create_connection():
    """ create a database connection to a SQLite database
    specified by db_file
    :param db_file: database file
    :return: Connection object or None
     """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(create_table_sql):
    """
    create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(create_table_sql)

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.commit()
            conn.close()


def create_user(username, password, salt):
    """
    create a new user to the user table
    :param username:
    :param password:
    :param salt:
    :return:
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('INSERT INTO users(username, password, salt) VALUES(?, ?, ?)', (username, password, salt))
        print("User was created successfully")

    except sqlite3.Error as e:
        print(e)

    finally:
        if conn:
            conn.commit()
            conn.close()


def delete_user(username):
    """
    remove user from USERS table in database
    :param conn:
    :param username:
    :return:
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('DELETE from users where username = ?', (username, ))
        print("User deleted successfully")

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.commit()
            #conn.close()


def change_password(username, new_password, new_salt):
    """
    change password for user in USERS table in database
    :param username:
    :param new_password:
    :param new_salt:
    :return:
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('UPDATE users set password = ? , SALT = ? where username = ?', (new_password, new_salt, username, ))

        print("password changed successfully")

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.commit()
            conn.close()


def get_user(username):
    """
    returns a row in database for given username
    if user doesnt exist returns None
    :param username:
    :return:
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM USERS WHERE username = ?", (username, ))

        return result.fetchone()

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


def get_password(username):
    """
    returns tuple (password, salt) for given username from database
    if username doesnt exist returns None
    :param username:
    :return:
    """
    user = get_user(username)
    if user is not None:
        return user[1], user[2]
    else:
        return None


def is_username_taken(username):
    """
    checks if given username is already taken
    returns True if taken, False otherwise
    :param username:
    :return:
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = ?", (username, ))

        return len(list(result)) > 0

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


def main():
    #database = r"D:\Game_Launcher\DB.db"

    sql_create_users_table = "CREATE TABLE IF NOT EXISTS users (" \
                             "username TEXT PRIMARY KEY," \
                             "password TEXT," \
                             "salt TEXT" \
                             ");"

    #create a database connection
    conn = create_connection()

    #create table
    if conn is not None:
        #create users table
        create_table(sql_create_users_table)
    else:
        print("Error! cannot create the database connection.")




if __name__ == '__main__':
    main()



