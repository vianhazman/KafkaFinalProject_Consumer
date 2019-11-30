from kafka import KafkaConsumer
from json import loads 

consumer = KafkaConsumer(
    'trackingtj',
    bootstrap_servers=['192.168.43.34:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: loads(x.decode('utf-8')))
for a in consumer:
    print(a.value)