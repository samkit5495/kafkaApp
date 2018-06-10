from kafka import KafkaConsumer
import json

from kafka import KafkaConsumer,KafkaProducer,TopicPartition
import threading, time
from dashboard.models import Transaction
from datetime import datetime
from mongoengine import connect
connect('dbtransactions')

consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                    group_id='test-group',
                    value_deserializer=lambda m: json.loads(m.decode('ascii')))
consumer.assign([TopicPartition('transactions',0)])
 
def consumerTask(data):
	user_id = int(data['id'])
	date = datetime.strptime(data['date'],'%d%b%Y')
	amount = float(data['amount']) if data['type'] is u'C' else -float(data['amount'])
	Transaction(
		user=user_id,
		date=date,
		amount=amount
		).save()
	balance_amount = Transaction.objects(user=user_id).sum('amount')
	# avg_pipeline = [
	#     {
	#         '$project':{
	#             '$avg':{
	#                 '$abs':'$amount'
	#             }
	#         }
	#     },
	#     {
	#         '$match':{
	#             {
	#                 'user':{
	#                     '$eq': user_id
	#                 }
	#             }
	#         }
	#     }
	# ]
	# average_txn_amount = list(Transaction.objects.aggregate(*avg_pipeline))[0]
	print(user_id, balance_amount)

for message in consumer:
  	print (message)
	consumerTask(message.value)
