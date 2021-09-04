import pika
from main import Product, db

params = pika.URLParameters(
    'amqps://bsuhqhfp:xbqSP5Cp7OWLT7z7Q8I3t9pzVvNQrmmS@rat.rmq2.cloudamqp.com/bsuhqhfp'
)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main', durable=True)


def callback(ch, method, properties, body):
    print('Recieved in main')
    data = json.loads(body)
    print(body)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'],
                          title=data['title'],
                          image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product Created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data['id'])
        db.session.delete(product)
        db.session.commit()
        print('Product Deleted')


channel.basic_consume(queue='main',
                      on_message_callback=callback,
                      auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()