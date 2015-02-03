#!/usr/bin/env python

import os
import sqlite3

from log import LOGGER
import conf



def init_db():
    '''
    this method must be called at the beginning of the server code.
    connects to pychat.db and create the users table
    '''
    LOGGER.info(" [.] init_db")
    conn = sqlite3.connect(conf.PYCHAT_DB)
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE if not exists users
                 (username text, realname text, email text, pubkey text)''')
    conn.close()


def reset_db():
    '''
    remove the pychat.db and creates a new one(calls create_db)
    '''
    LOGGER.info(" [.] reset_db")
    os.system('rm -rf %s' % conf.PYCHAT_DB)
    create_db()

    
def add_user(username, realname, email, pubkey):
    '''
    adds a new user to the pychat.db users table.

    : name : string  (can be anything really)
    : email : string  (can be anything really)
    : pubkey : ascii armored gnupg public key for the user
    '''
    LOGGER.info(" [.] add_user (%s, %s, %s, %s)" % (username,realname,email,pubkey,))
    conn = sqlite3.connect(conf.PYCHAT_DB)
    c = conn.cursor()


    # Create table

    c.execute('''INSERT INTO users VALUES (?, ?, ?, ?)''',(username, realname, email, pubkey,))
    LOGGER.debug(" [.] insert into users execute successful")
    conn.commit()
    LOGGER.debug(" [.] commit successful")

    conn.close()


def get_users():
    '''
    get all the users that are registered in the system.
    '''
    conn = sqlite3.connect(conf.PYCHAT_DB)
    c = conn.cursor()

    c.execute('''SELECT * FROM users''')

    users = c.fetchall()
    conn.close()
 
    return users
   


if __name__ == '__main__':
    conf.PYCHAT_DB = 'test_pychat.db'
    reset_db()
    
