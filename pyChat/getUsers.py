#!/usr/bin/env python

import pika
import uuid
import crypto


class pychat_server(object):
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

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
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


if __name__ == '__main__':
    import log

    test = pychat_server('localhost')

    # get pubkey
    # login to server
    # get all users

    key = crypto.genkey('tester')

    log.log.debug(" [.] Requesting add_users on localhost")
    response = test.call("add_user|tester|real tester name|tester@g.com|%s" % key)
    

    log.log.debug(" [.] Requesting GetUsers() on localhost")
    response = test.call("get_users")
    log.log.debug(" [+] Got (%s)" % (response,))
