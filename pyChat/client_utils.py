#!/usr/bin/env python

import pika
import uuid
import crypto
import log
import json


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
 
            server_pubkey = self.call("server_pubkey")
            log.log.debug(" [+] Requested server pubkey (%s)" % (server_pubkey,))
                self.val = None

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
            pychat_server.instance = pychat_server.__OnlyOne(arg)


    def getUsers(self):
        '''
        Constructs the message to send to the server and retrieves the users list from the server
        '''
        log.log.info(" [.] Requesting GetUsers() on localhost")
        response = self.instance.server_call("get_users")
        log.log.debug(" [.] GetUsers() response (%s)", (response,))
        return json.loads(response)
    

    def login(self,user,keyid):
        '''
        logs into the server... required for receiving messages.
        '''
        log.log.info(" [.] Requesting GetUsers() on localhost")
        suser=crypto.sign(user,keyid)
        response = self.instance.server_call("login|{0}".format(suser))
        log.log.debug(" [.] GetUsers() response (%s)", (response,))
        return json.loads(response)
    

    def sendmsg(user, msg):
        '''
        tries to put the message in the users queue
        '''
        self.instance.rabbitmq_publish(user, msg)


if __name__ == '__main__':
    import log

    test = pychat_server('localhost')

    # get pubkey
    # login to server
    # get all users

    key = crypto.genkey('tester')

    log.log.debug(" [.] Requesting add_users on localhost")
    response = test.server_call("add_user|tester|real tester name|tester@g.com|%s" % key)

    log.log.debug(" [.] Requesting GetUsers() on localhost")
    response = test.server_call("get_users")
    log.log.debug(" [+] Got (%s)" % (response,))
