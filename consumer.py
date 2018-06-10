from kafka import KafkaConsumer
import json

from kafka import KafkaConsumer,KafkaProducer,TopicPartition
import threading, time
from dashboard.models import Transaction, User
from datetime import datetime
from math import sqrt
import statistics
from mongoengine import connect
from bson import ObjectId

connect('dbtransactions-user-stats')

consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                    group_id='test-group',
                    value_deserializer=lambda m: json.loads(m)
										)
consumer.assign([TopicPartition('transactions',0)])
 
def cal_avg_txn_amount(user):
	avg_txn_amount_pipeline = [
	    {
	        '$group':{
	            '_id':'$user',
                    'avgTxn':{
                        '$avg':{
                            '$abs':'$amount'
                        }
                    }
	        }
	    },
	    {
	        '$match':{
	                '_id':{
	                    '$eq': ObjectId(user.id)
	                }
	        }
	    }
	]
	try:
		avg_txn_amount = list(Transaction.objects.aggregate(*avg_txn_amount_pipeline))[0]['avgTxn']
		return avg_txn_amount
	except:
		return 0


def cal_avg_monthly_bal_amount(user):
	avg_monthly_bal_amount_pipeline = [
	    {
	        '$group':{
	            '_id':{
                        'user':'$user',
                        'month':{'$month': '$date'}
                        },
                    'monthlyBal':{
                        '$sum':'$amount'
                        }
	        }
	    },
            {
	         '$match':{
                     '_id.user':{
                         '$eq': ObjectId(user.id)
                     }
	         }
	     }
	]
	try:
		monthly_bal = [i['monthlyBal'] for i in list(Transaction.objects.aggregate(*avg_monthly_bal_amount_pipeline))]
		avg_monthly_bal_amount = sum(monthly_bal)/len(monthly_bal)
		return avg_monthly_bal_amount
	except:
		return 0

def calculate_standard_deviation(user):
	x = [i.amount for i in Transaction.objects(user=user).only('amount')]
	try:
		return statistics.stdev(x)
	except:
		return float('inf')

def get_user(user_id):
	user = User.objects(user_id=user_id)
	if user:
		user = user.first()
	else:
		user = User(user_id=user_id).save()
	return user


def consumerTask(data):
	user_id = int(data['id'])
	date = datetime.strptime(data['date'],'%d%b%Y')
	amount = float(data['amount']) if data['type'] == u'D' else -float(data['amount'])
	# Maintain a total balance,
	user = get_user(user_id)
	balance_amount = Transaction.objects(user=user).sum('amount')
	#  average transaction amount,
	avg_txn_amount = cal_avg_txn_amount(user)
	# standard deviation of transaction amount
	standard_deviation = calculate_standard_deviation(user)
	#  Average monthly balance.
	avg_monthly_balance = cal_avg_monthly_bal_amount(user)
	alert = abs(amount) > 2 * standard_deviation 
	user.update(
		user_id=user_id,
		balance = balance_amount,
		avg_transaction_amount=avg_txn_amount,
		stdev=standard_deviation,
		avg_monthly_balance = avg_monthly_balance
		)
	# Maintain transaction log for each and every user.
	Transaction(
		user=user,
		date=date,
		amount=amount,
		alert=alert
		).save()
	print(user_id, balance_amount, avg_txn_amount, standard_deviation, avg_monthly_balance, alert)

for message in consumer:
	consumerTask(message.value)
