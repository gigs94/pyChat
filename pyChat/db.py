#!/usr/bin/env python

import os
import sqlite3

PYCHAT_DB = 'pychat.db'


def reset_db():
    '''
    remove the pychat.db and creates a new one(calls create_db)
    '''
    os.system('rm -rf %s' % PYCHAT_DB)
    create_db()

    
def create_db():
    '''
    connects to pychat.db and create the users table
    '''
    conn = sqlite3.connect(PYCHAT_DB)
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE users
                 (name text, email text, pubkey text)''')
    conn.close()


def add_user(name, email, pubkey):
    '''
    adds a new user to the pychat.db users table.

    : name : string  (can be anything really)
    : email : string  (can be anything really)
    : pubkey : ascii armored gnupg public key for the user
    '''
    conn = sqlite3.connect(PYCHAT_DB)
    c = conn.cursor()

    # Create table
    c.execute('''INSERT INTO users
                 (%s, %s, %s)''' % name, email, pubkey)

    conn.close()


def get_users():
    conn = sqlite3.connect(PYCHAT_DB)
    c = conn.cursor()

    # Create table
    c.execute('''SELECT * FROM users''')

    users = c.fetchall()
    conn.close()
 
    return users
   


if __name__ == '__main__':
    reset_db()
