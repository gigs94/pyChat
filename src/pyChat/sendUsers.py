#!/usr/bin/env python


import pika
import pyChat_log
import pyChat_crypto


#-------------------------------------------------------------
def adduser(user):
    '''
    adduser takes the username, password, email, realname
    '''
    # TODO implement this method.
    return "user added successfully"

    

def add_user(ch, method, props, n):
    '''
    handle message of type add_user by processing the messgae and returning
    whether the action was successful or not.
    '''
    pyChat_log.log.info(" [.] add_user requested(%s)" % (n,))

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

    # TODO implement this method.
    return "joe bob"


def get_users(ch, method, props, n):
    pyChat_log.log.info(" [.] get_users requested with filter(%s)" % (n,))
    response = getusers(n)
    pyChat_log.log.debug("    [-] response(%s)" % (response,))

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))

    pyChat_log.log.debug("    [-] response(%s)" % (response,))

    ch.basic_ack(delivery_tag = method.delivery_tag)



#-------------------------------------------------------------
def login(ch, method, props, n):
    '''
    validates username/password and creates queue for them to receive messages
    '''
    # TODO 
    pass



def logoff(ch, method, props, n):
    '''
    signs off the user and removes the queue
    '''
    # TODO 
    pass



#-------------------------------------------------------------
def server_pubkey():
    pass



def get_server_pubkey(ch, method, props, n):
    '''
    returns the gnupg pubkey for the server
    '''
    pyChat_log.log.info(" [.] get_server_pubkey requested(%s)" % (n,))

    response = pyChat_crypto.getkey(n)

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
    pyChat_log.log.info(" [.] server_queue received message (%s)" % (body,))

    if n[0] == 'get_users':
        get_users(ch, method, props, n[1:])
    
    elif n[0] == 'add_user':
        get_users(ch, method, props, n[1:])

    elif n[0] == 'server_pubkey':
        get_server_pubkey(ch, method, props, n[1:])

    elif n[0] == 'login':
        login(ch, method, props, n[1:])

    elif n[0] == 'logoff':
        logoff(ch, method, props, n[1:])

    else:
        pyChat_log.log.critical(" [.] server_queue received INVALID MESSAGE (%s) ignoring" % (body,))
        ch.basic_ack(delivery_tag = method.delivery_tag)
        
    


#-------------------------------------------------------------
def run_server():
    '''
    Starts the queue to listen for server messages, then processes them accordingly.
    '''
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))

    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue='server_queue')
    channel.basic_consume(server_queue, queue='server_queue')

    pyChat_log.log.debug(" [x] Awaiting server_queue requests")

    channel.start_consuming()



#-------------------------------------------------------------
if __name__ == '__main__':
    run_server()
