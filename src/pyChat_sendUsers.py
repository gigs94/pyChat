#!/usr/bin/env python

import pika
import pyChat_log


def adduser(user):
    '''
    '''

    

def getusers(pattern):
    '''
    getusers(pattern) queries the registered users for a patter or returns all users if ""

    TODO pattern not implemented yet, but it should be a regex to filter users to be returned
    '''
    # TODO implement this method.
    return "joe bob"

def on_AddUser(ch, method, props, body):
    pass


def server_queue(ch, method, props, body):
    '''
    server_queue(ch, method, props, body) is a callback for when messages are found on the server_queue queue
    '''
    n = body.split('|')


    if n[0] == 'get_users':
        get_users(ch, method, props, n[1:])
    
    if n[0] == 'add_user':
        get_users(ch, method, props, n[1:])
    


def get_users(ch, method, props, n):
    pyChat_log.log.debug(" [.] get_users requested(%s)" % (n,))
    response = getusers(n)
    pyChat_log.log.debug("    [.] response(%s)" % (response,))

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)


def add_user(ch, method, props, n):
    pyChat_log.log.debug(" [.] add_user requested(%s)" % (n,))
    response = adduser(n)

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
    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue='server_queue')
    channel.basic_consume(server_queue, queue='server_queue')

    pyChat_log.log.debug(" [x] Awaiting server_queue requests")

    channel.start_consuming()


if __name__ == '__main__':
    
    run_server()
