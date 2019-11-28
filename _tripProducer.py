from kafka import KafkaProducer
from json import dumps
from time import sleep
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: 
    dumps(x).encode('utf-8'))

with open('trip.json') as json_file:
    data = json.load(json_file)
    
    while True:
        for p in data['data']:
            print(p)
            producer.send('testkafka', value=p)
            sleep(2)


# for e in range(1000):
#     data = {'number' : e}
#     producer.send('transjakarta', value=data)
#     sleep(2)