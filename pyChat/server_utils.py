#!/usr/bin/env python


import pika
import log
import crypto
import db
import json


#-------------------------------------------------------------
def adduser(info):
    '''
    adds a new user to the system
    : info : an array of username, realname, email and pubkey 
    '''
    db.add_user(info[0], info[1], info[2], info[3])
    return "user added successfully"

    

def add_user(ch, method, props, n):
    '''
    handle message of type add_user by processing the messgae and returning
    whether the action was successful or not.
    '''
    log.log.info(" [.] add_user requested(%s)" % (n,))

    response = adduser(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))

    ch.basic_ack(delivery_tag = method.delivery_tag)



#-------------------------------------------------------------
def getusers(pattern):
    '''
    getusers(pattern) queries the registered users for a patter or returns all users if ""

    TODO pattern not implemented yet, but it should be a regex to filter users to be returned
    '''

    return db.get_users()


def get_users(ch, method, props, n):
    log.log.info(" [.] get_users requested with filter(%s)" % (n,))
    response = getusers(n)
    log.log.debug("    [-] response(%s)" % (response,))

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=json.dumps(response))

    log.log.debug("    [-] response(%s)" % (response,))

    ch.basic_ack(delivery_tag = method.delivery_tag)



#-------------------------------------------------------------
def log_on_off(ch, method, props, n):
    '''
    internal method that does common functionality between logon and logoff
    it verifies the signature of the username and deletes the queue for that
    user.
    : return : channel associated with the username which should have been deleted at the end of this method
    '''
    if not crypto.verify(n):
        log.log.debug("    [-] verification of signature failed for (%s)" % (n,))
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

    return channel


def login(ch, method, props, n):
    '''
    validates username/password and creates queue for them to receive messages
    '''
    channel = log_on_off(ch, method, props, n)
    channel.queue_declare(queue=username)



def logoff(ch, method, props, n):
    '''
    signs off the user and removes the queue
    '''
    log_on_off(ch, method, props, n)



#-------------------------------------------------------------
def get_server_pubkey(ch, method, props, n):
    '''
    returns the gnupg pubkey for the server
    '''
    log.log.info(" [.] get_server_pubkey requested(%s)" % (n,))

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
    log.log.info(" [.] server_queue received message")
    log.log.debug(" [-] message body (%s)" % (body,))

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
        log.log.critical(" [.] server_queue received INVALID MESSAGE (%s) ignoring" % (body,))
        ch.basic_ack(delivery_tag = method.delivery_tag)
        
    



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

    log.log.debug(" [x] Awaiting server_queue requests")

    channel.start_consuming()



#-------------------------------------------------------------
if __name__ == '__main__':
    run_server()
