import pika, json, os, django
from products.models import Product

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

params = pika.URLParameters(
    'amqps://bsuhqhfp:xbqSP5Cp7OWLT7z7Q8I3t9pzVvNQrmmS@rat.rmq2.cloudamqp.com/bsuhqhfp'
)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin', durable=True)


def callback(ch, method, properties, body):
    print('Recieved in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased')


channel.basic_consume(queue='admin',
                      on_message_callback=callback,
                      auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()