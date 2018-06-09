import threading, logging, time
import multiprocessing
 
from kafka import KafkaConsumer, TopicPartition
import json
from dashboard.models import Transactions
from datetime import datetime
from mongoengine import connect
connect('dbtransactions')

class Consumer(multiprocessing.Process):
    def __init__(self, num):
        self.num= num
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
         
    def stop(self):
        self.stop_event.set()

    def consumerTask(self, data):
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

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                             group_id='test-group',
                             value_deserializer=lambda m: json.loads(m.decode('ascii')))
        consumer.subscribe(['transactions'])
        while not self.stop_event.is_set():
            for message in consumer:
                self.consumerTask(message.value)
                if self.stop_event.is_set():
                    break
 
        consumer.close()
         
         
def main():
    tasks = [
        Consumer(0),
        # Consumer(1)
    ]
 
    for t in tasks:
        t.start()
  
    for task in tasks:
        task.join()
         
         
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()