#!/usr/bin/env python

'''
Description:
        client_utils contains a singleton class, pychat_server, which is to be used to 
        interface with the server.   It contains all the comms and protocol for dealing
        with the server.   Any new client programs should use this class to interact with
        the pyChat system.

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
import uuid
import crypto
from log import LOGGER
import json
from read_messages import ReadMessages
from collections import deque


class pychat_server(object):
    '''
    A singleton class that interfaces with the server.
    '''
    class __OnlyOne:
        def __init__(self, host):
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host=host))

            self.channel = self.connection.channel()

            result = self.channel.queue_declare(exclusive=True)
            self.callback_queue = result.method.queue

            self.channel.basic_consume(self.on_response, no_ack=True,
                                       queue=self.callback_queue)
 
            server_pubkey = self.server_call("server_pubkey")
            LOGGER.debug(" [+] Requested server pubkey (%s)" % (server_pubkey,))
            self.val = None
            self.run_thread = None

            self.queue = deque()
            self.whoami = None

        def get_whoami(self):
            return self.whoami

        def login(self, user):
            self.whoami = user

        def stop(self):
            self.run_thread.stop()

        def on_response(self, ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = body

        def server_call(self, n):
            '''
            Creates a server_queue message, sends it, and waits for response
            '''
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(exchange='',
                                       routing_key='server_queue',
                                       properties=pika.BasicProperties(
                                             reply_to = self.callback_queue,
                                             correlation_id = self.corr_id,
                                             ),
                                       body=str(n))
            while self.response is None:
                self.connection.process_data_events()
            return self.response


        def read_queue(self, username):
            '''
            Start a new thread that will get messages for the logged in user
            '''
            self.run_thread = ReadMessages('localhost', username, self.queue.append)
            self.run_thread.start()

        def stop(self):
            if self.run_thread is not None:
                self.run_thread.stop()


        def decrypt_inbound(self,body):
            '''
            takes a user message and tries to decrypt the body of the message

            :rtype: tuple of user, decrypted body, and original body
            '''
            user,msg = body.split('|')
            decrypted = crypto.decrypt(msg)
            return (user,decrypted,msg)

        def getusers_messages(self):
            messages = []
            while (True):
                if len(self.queue) != 0:
                   user,msg,orig = self.decrypt_inbound(self.queue.popleft())
                   messages.append("{0}|{1}".format(user,msg))
                else:
                   break

            return messages


        def getusers_messages(self, user):
            messages = []
            while (True):
                if len(self.queue) != 0:
                   ruser,msg,orig = self.decrypt_inbound(self.queue.popleft())
                   if ruser == user:
                       messages.append(msg)
                   else:
                       # This is a really a hack, but it works :)
                       self.queue.append("{0}|{1}".format(user,orig))
                else:
                   break
            return messages


        def rabbitmq_publish(self, queue, msg):
            '''
            Publishes to the queue
            '''
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(exchange='',
                                       routing_key=queue,
                                       properties=pika.BasicProperties(
                                             correlation_id = self.corr_id,
                                             ),
                                       body=str(msg))



    #------------------------------------------------------------
    instance = None


    def __init__(self, host):
        if not pychat_server.instance:
            pychat_server.instance = pychat_server.__OnlyOne(host)


    def getUsers(self):
        '''
        Constructs the message to send to the server and retrieves the users list from the server
        '''
        LOGGER.info(" [.] Requesting GetUsers() on localhost")
        response = self.instance.server_call("get_users")
        LOGGER.debug(" [.] GetUsers() response (%s)", (response,))
        jresponse = json.loads(response)
        for j in jresponse:
            crypto.import_keys(j[3])
        return jresponse
    

    def login(self,user):
        '''
        logs into the server... required for receiving messages.  And starts the read_queue thread.
        '''
        LOGGER.info(" [.] Logging in user ({0})".format(user))
        suser=crypto.sign(user,user)
        response = self.instance.server_call("login|{0}".format(suser))
        LOGGER.debug(" [.]     response (%s)", (response,))

        # Start up the read_queue to getting messages
        self.instance.read_queue(user)
        rtn = False
        if response == 'user logged in succesfully':
            self.instance.login(user)
            rtn = True
        return rtn    


    def logoff(self,user):
        '''
        logs off of the server... required for receiving messages.
        '''
        LOGGER.info(" [.] Logging off user ({0})".format(user))
        suser=crypto.sign(user,user)
        response = self.instance.server_call("logoff|{0}".format(suser))
        LOGGER.debug(" [.]     response (%s)", (response,))
        return (response == 'user logged off succesfully')
    

    def register(self,user, realname, email, key):
        '''
        registers new username with the server.
        '''
        LOGGER.info(" [.] Registering {0}, {1}, {2}, {3}".format(user, realname, email, key))
        suser=crypto.sign(user,user)
        sreal=crypto.sign(realname,user)
        semail=crypto.sign(email,user)
        response = self.instance.server_call("add_user|{0}|{1}|{2}|{3}".format(suser,sreal,semail,key))
        LOGGER.debug(" [.]     response (%s)", (response,))
        return (response == 'user added successfully') 


    def sendmsg(self, user, msg):
        '''
        tries to put the message in the users queue
        '''
        LOGGER.info(" [.] Publishing message ({0}) to user ({1})".format(msg,user))
        foo = crypto.encrypt(msg, [user])
        body = "{0}|{1}".format(self.instance.get_whoami(),foo)
        self.instance.rabbitmq_publish(user, body)


    def readmsg(self):
        '''
        tries to put the message in the users queue
        '''
        LOGGER.info(" [.] Getting messages")
        return self.instance.getusers_messages()


    def readmsg(self, user):
        '''
        gets message in the users queue from a specific user
        '''
        LOGGER.info(" [.] Getting messages")
        return self.instance.getusers_messages(user)


    def stop(self):
        LOGGER.info(" [.] Stopping the process")
        self.instance.stop()
