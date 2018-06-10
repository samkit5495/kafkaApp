# kafkaApp
A sample application which connects with kafka and produces &amp; consumes data, and shows analysis on a dashboard using Django framework

Kafka Installation:

Reference : https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-14-04

Kafka Consumer/Producers:

https://github.com/Parsely/pykafka/blob/master/README.rst
http://kafka-python.readthedocs.io/


#Note:

Refer consumer.py for consumer and others tried examples are in consumer folder

#How to Run Project:

1. Start Zookeeper
```
bin/zookeeper-server-start.sh config/zookeeper.properties
```
2. Start Kafka Server
```
nohup ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties > ~/kafka/kafka.log 2>&1 &
```
3. Start MongoDB on default port 27017
```
mongod --dbpath "$PWD"
```
4. Setup Virtual Environment
```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
4. Start publisher.py
```
python3 publisher.py
```
5. Start consumer.py
```
python3 consumer.py
```
6. Start Django Server
```
python3 manage.py runserver
```