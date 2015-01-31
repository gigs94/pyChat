import pika
import uuid

#-------------------------------------------------------------
def sendmsg(user, msg):
    '''
    tries to put the message in the users queue
    '''
    response = None
    corr_id = str(uuid.uuid4())

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()
    channel.basic_publish(exchange='',
                          routing_key=user,
                          properties=pika.BasicProperties(
                              correlation_id = corr_id,
                          ),
                          body=str(msg))
