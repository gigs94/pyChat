#!/usr/bin/env python
import pika
import pyChat_log


def getusers(pattern):
    '''
    getusers(pattern) queries the registered users for a patter or returns all users if ""

    TODO pattern not implemented yet, but it should be a regex to filter users to be returned
    '''
    # TODO implement this method.
    return "joe bob"

def on_GetUsers(ch, method, props, body):
    '''
    on_GetUsers(ch, method, props, body) is a callback for when messages are found on the getUsers queue
    '''
    n = int(body)

    logging.debug(" [.] GetUsers requested(%s)".format(n,))
    response = getusers(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)


def run_server():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='getUsers')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_GetUsers, queue='getUsers')

    logging.debug(" [x] Awaiting getUsers requests")
    channel.start_consuming()


if __name__ == '__main__':
    
    run_serer()
