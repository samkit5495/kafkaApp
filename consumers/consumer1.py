import threading, logging, time
import multiprocessing
 
from kafka import KafkaConsumer, TopicPartition
import json

class Consumer(multiprocessing.Process):
    def __init__(self, num):
        self.num= num
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
         
    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                             group_id='test-group',
                             value_deserializer=lambda m: json.loads(m.decode('ascii')))
        consumer.subscribe(['transactions'])
        while not self.stop_event.is_set():
            for message in consumer:
                if self.stop_event.is_set():
                    break
 
        consumer.close()
         
         
def main():
    tasks = [
        Consumer(0),
        Consumer(1)
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