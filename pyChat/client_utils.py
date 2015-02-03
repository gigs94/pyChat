#!/usr/bin/env python

import pika
import uuid
import crypto
import log
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
            log.log.debug(" [+] Requested server pubkey (%s)" % (server_pubkey,))
            self.val = None
            self.run_thread = None

            self.queue = deque()

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


        def getusers_messages(self):
            messages = []
            while (True):
                if len(self.queue) != 0:
                   msg = self.queue.popleft()
                   messages.append(msg)
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
        log.log.info(" [.] Requesting GetUsers() on localhost")
        response = self.instance.server_call("get_users")
        log.log.debug(" [.] GetUsers() response (%s)", (response,))
        return json.loads(response)
    

    def login(self,user):
        '''
        logs into the server... required for receiving messages.
        '''
        log.log.info(" [.] Logging in user ({0})".format(user))
        suser=crypto.sign(user,user)
        response = self.instance.server_call("login|{0}".format(suser))
        log.log.debug(" [.]     response (%s)", (response,))
        self.instance.read_queue(user)
        return (response == 'user logged in succesfully')


    def logoff(self,user):
        '''
        logs off of the server... required for receiving messages.
        '''
        log.log.info(" [.] Logging off user ({0})".format(user))
        suser=crypto.sign(user,user)
        response = self.instance.server_call("logoff|{0}".format(suser))
        log.log.debug(" [.]     response (%s)", (response,))
        return (response == 'user logged off succesfully')
    

    def register(self,user, realname, email, key):
        '''
        registers new username with the server.
        '''
        log.log.info(" [.] Registering {0}, {1}, {2}, {3}".format(user, realname, email, key))
        suser=crypto.sign(user,user)
        sreal=crypto.sign(realname,user)
        semail=crypto.sign(email,user)
        response = self.instance.server_call("add_user|{0}|{1}|{2}|{3}".format(suser,sreal,semail,key))
        log.log.debug(" [.]     response (%s)", (response,))
        return (response == 'user added successfully') 


    def sendmsg(self, user, msg):
        '''
        tries to put the message in the users queue
        '''
        log.log.info(" [.] Publishing message ({0}) to user ({1})".format(msg,user))
        self.instance.rabbitmq_publish(user, msg)


    def readmsg(self):
        '''
        tries to put the message in the users queue
        '''
        log.log.info(" [.] Getting messages")
        return self.instance.getusers_messages()


    def stop(self):
        log.log.info(" [.] Stopping the process")
        self.instance.stop()
