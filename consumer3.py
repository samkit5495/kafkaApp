from confluent_kafka import Consumer, KafkaError


c = Consumer({
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'mygroup',
    'default.topic.config': {
        'auto.offset.reset': 'smallest'
    }
})

c.subscribe(['transactions'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()