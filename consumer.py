from kafka import KafkaConsumer
import json

from kafka import KafkaConsumer,KafkaProducer,TopicPartition
import threading, time
from dashboard.models import Transactions
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
	amount = float(data['amount']) if data['type'] is 'D' else -float(data['amount'])
	Transactions(
		user=user_id,
		date=date,
		amount=amount
		).save()
	balance_amount = Transactions.objects(user=user_id).sum('amount')
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
	# average_txn_amount = list(Transactions.objects.aggregate(*avg_pipeline))[0]
	print(data.id, balance_amount)

for message in consumer:
  	print (message)
