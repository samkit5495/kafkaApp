from kafka import KafkaProducer
import json

# producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))

with open('sample_data.csv') as f:
    lines = f.readlines()
for line in lines:
    data = line.replace('\r\n','').split(',')
    data = {
        'id':data[0],
        'date':data[1],
        'type':data[2],
        'amount':data[3]
    }
    producer.send('transactions', data)
producer.flush()