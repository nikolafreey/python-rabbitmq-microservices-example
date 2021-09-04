import pika
import json

params = pika.URLParameters(
    'amqps://bsuhqhfp:xbqSP5Cp7OWLT7z7Q8I3t9pzVvNQrmmS@rat.rmq2.cloudamqp.com/bsuhqhfp'
)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='',
                          routing_key='admin',
                          body=json.dumps(body),
                          properties=properties)
