from kafka import KafkaConsumer
import json

from kafka import KafkaConsumer,KafkaProducer,TopicPartition
import threading, time
 
class Consumer(threading.Thread):
  daemon = True
  def __init__(self, num):
    self.num = num
    self.count = 0
    threading.Thread.__init__(self)
    self.consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                             group_id='test-group',
                             value_deserializer=lambda m: json.loads(m.decode('ascii')))
    self.consumer.assign([TopicPartition('transactions',num)])
 
  def run(self):
    for message in self.consumer:
      self.count+=1
      print (message,self.num, self.count)
 
if __name__ == "__main__":
  threads = [
    Consumer(0),
    Consumer(1)
  ]
  for t in threads:
    t.start()
  while True:
    time.sleep(10)