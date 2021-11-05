from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
from time import sleep
import os

kafka_url = os.environ.get('KAFKA_URL')  # localhost:9092
mongo_url = os.environ.get('MONGO_URL')  # localhost:27017
mongo_user = os.environ.get('MONGO_USER')  # root
mongo_pass = os.environ.get('MONGO_PASS')  # pass12345
print("kafka_url =", kafka_url)
print("mongo_url =", mongo_url)
consumer = ''

tries = 0
while tries < 6:
    try:
        print("Attempting to connect to kafka...")
        consumer = KafkaConsumer(
            'purchases',
            bootstrap_servers=[kafka_url],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: loads(x.decode('utf-8')))
        break
    except:
        tries += 1
        sleep(10)

if tries == 6:
    raise ConnectionError("Couldn't connect to kafka")
else:
    print("Connected to kafka!")

client = MongoClient(mongo_url,
                     username=mongo_user,
                     password=mongo_pass)
collection = client.purchases.history

for message in consumer:
    message = message.value
    collection.insert_one(message)
    print('{} added to {}'.format(message, collection))
