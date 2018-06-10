from kafka import KafkaProducer
import json
from datetime import datetime

# producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))

with open('sample_data.csv') as f:
    lines = f.readlines()
month = 1
for line in lines:
    data = line.replace('\r\n','').split(',')
    data = {
        'id':data[0],
        'date':data[1],
        'type':data[2],
        'amount':data[3]
    }
    new_month = datetime.strptime(data['date'],'%d%b%Y').month
    if month!=new_month:
        if input('New Month:'+str(new_month)+' Enter 1 to continue and 0 to exit: ') != 1:
            break
        month = new_month
    producer.send('transactions', data)
producer.flush()