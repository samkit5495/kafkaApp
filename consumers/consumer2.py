from pykafka import KafkaClient

client = KafkaClient(hosts="127.0.0.1:9092")

client.topics
topic = client.topics['transactions']

balanced_consumer = topic.get_balanced_consumer(
    consumer_group='testgroup',
    auto_commit_enable=True,
    zookeeper_connect='localhost:2181'
)

for message in balanced_consumer:
     if message is not None:
        print message.offset, message.value