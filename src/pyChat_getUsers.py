#!/usr/bin/env python
import pika
import uuid

class GetUsers(object):
    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=host))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='getUsers',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str())
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


if __name__ == '__main__':
    test = GetUsers('localhost')

    print " [x] Requesting GetUsers() on localhost"
    response = test.call()
    print " [.] Got %r" % (response,)
