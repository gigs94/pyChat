#!/usr/bin/env python
'''
Description:
        server_utils.   This is the code that runs the server.  The server implementation
        just calls run_server()

Author:
        Daniel Gregory (gigs94@gmail.com)

Licence:
        The MIT License (MIT)

        Copyright (c) 2015 Daniel Gregory

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in
        all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
        THE SOFTWARE.
'''


import pika
import logging
from log import LOGGER
import crypto
import db
import json

import time # TODO


#-------------------------------------------------------------
def adduser(user,real,email,key):
    '''
    adds a new user to the system
    : info : an array of username, realname, email and pubkey 
    '''
    # TODO -- add capability to "reregister" (lost key file, etc...)

    rtn = None

    nkey = crypto.getkey(user)
    if nkey == '':
        crypto.import_keys(key)
        db.add_user(user,real,email,key)
        rtn = "user added successfully"
    else:
        rtn = "user (%s) already exists.  Please select another username".format(user)
        LOGGER.critical(rtn)
    
    return rtn

    

def add_user(ch, method, props, n):
    '''
    handle message of type add_user by processing the messgae and returning
    whether the action was successful or not.
    '''
    LOGGER.info(" [.] add_user requested(%s)" % (n,))

    
    if crypto.verify(n[0]):
        user=crypto.decrypt(n[0])
    if crypto.verify(n[1]):
        real=crypto.decrypt(n[1])
    if crypto.verify(n[2]):
        email=crypto.decrypt(n[2])
    key=n[3]

    LOGGER.info(" [.] adding user, realname, email (%s,%s,%s)" % (user,real,email,))

    response = adduser(user,real,email,key)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))

    ch.basic_ack(delivery_tag = method.delivery_tag)



#-------------------------------------------------------------
def get_users_from_db(pattern):
    '''
    get_users_from_db(pattern) queries the registered users for a patter or returns all users if ""

    TODO pattern not implemented yet, but it should be a regex to filter users to be returned
    '''

    return db.get_users()


def get_users(ch, method, props, n):
    '''
    return a list of users based on a pattern n
    '''
    LOGGER.info(" [.] get_users requested with filter(%s)" % (n,))
    response = get_users_from_db(n)
    LOGGER.debug("    [-] response(%s)" % (response,))

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=json.dumps(response))

    LOGGER.debug("    [-] response(%s)" % (response,))

    ch.basic_ack(delivery_tag = method.delivery_tag)



#-------------------------------------------------------------
def log_on_off(ch, method, props, n):
    '''
    internal method that does common functionality between logon and logoff
    it verifies the signature of the username and deletes the queue for that
    user.
    : return : the username that is being logged on/off
    '''
    if not crypto.verify(n):
        LOGGER.debug("    [-] verification of signature failed for (%s)" % (n,))
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                         body="FAILED")
    
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return
        
    username = crypto.decrypt(n)
        
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))

    channel = connection.channel()

    channel.basic_qos(prefetch_count=1)

    # get rid of any old requests
    channel.queue_delete(queue=username)

    return username


def login(ch, method, props, n):
    '''
    validates username/password and creates queue for them to receive messages
    '''
    username = str(n[0]).rstrip()
    username = log_on_off(ch, method, props, username)
    LOGGER.info(" [.] login (%s)" % (username,))
    ch.queue_declare(queue=username)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str('user logged in succesfully'))

    ch.basic_ack(delivery_tag = method.delivery_tag)


def logoff(ch, method, props, n):
    '''
    signs off the user and removes the queue
    '''
    LOGGER.info(" [.] logoff (%s)" % (n,))
    username = str(n[0]).rstrip()
    username = log_on_off(ch, method, props, username)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str('user {0} logged off succesfully'.format(username)))

    ch.basic_ack(delivery_tag = method.delivery_tag)


#-------------------------------------------------------------
def get_server_pubkey(ch, method, props, n):
    '''
    returns the gnupg pubkey for the server
    '''
    LOGGER.info(" [.] get_server_pubkey requested(%s)" % (n,))

    response = crypto.getkey(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))

    ch.basic_ack(delivery_tag = method.delivery_tag)


    
#-------------------------------------------------------------
def server_queue(ch, method, props, body):
    '''
    server_queue(ch, method, props, body) is a callback for when messages are found on the server_queue queue
    '''
    n = body.split('|')
    LOGGER.info(" [.] server_queue received message")
    LOGGER.debug(" [-] message body (%s)" % (body,))

    if n[0] == 'get_users':
        get_users(ch, method, props, n[1:])
    
    elif n[0] == 'add_user':
        add_user(ch, method, props, n[1:])

    elif n[0] == 'server_pubkey':
        get_server_pubkey(ch, method, props, n[1:])

    elif n[0] == 'login':
        login(ch, method, props, n[1:])

    elif n[0] == 'logoff':
        logoff(ch, method, props, n[1:])

    elif n[0] == 'sendmsg':
        sendmsg(ch, method, props, n[1:])

    else:
        LOGGER.critical(" [.] server_queue received INVALID MESSAGE (%s) ignoring" % (body,))
        ch.basic_ack(delivery_tag = method.delivery_tag)

    LOGGER.info(" [.] server_queue finished processing message")

    
        
    



#-------------------------------------------------------------
def run_server():
    '''
    Starts the queue (name=server_queue) to listen for server messages, then processes them accordingly.
    '''
    db.init_db()

    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))

    channel = connection.channel()

    channel.basic_qos(prefetch_count=1)

    # get rid of any old requests
    channel.queue_delete(queue='server_queue')
    channel.queue_declare(queue='server_queue')
    channel.basic_consume(server_queue, queue='server_queue')

    LOGGER.debug(" [x] Awaiting server_queue requests")

    channel.start_consuming()



#-------------------------------------------------------------
if __name__ == '__main__':
    LOGGER.setLevel(logging.DEBUG)
    run_server()
