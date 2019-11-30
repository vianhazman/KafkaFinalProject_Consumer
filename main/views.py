from django.shortcuts import render
from threading import Thread
import websocket
from websocket import create_connection
import time, json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from kafka import KafkaConsumer
from json import loads
from KafkaFinalProject_Consumer import settings

trackingThread = None
tripThread = None

def tracking_thread():
    consumer = KafkaConsumer(
        'trackingtj',
        bootstrap_servers=[settings.KAFKA_PRODUCER_IP+':9092'],
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    #dummy poll
    consumer.poll()
    #go to end of the stream
    consumer.seek_to_end()
    for message in consumer:
        print(message.value)
        try:
            channel_layer = get_channel_layer()
            if ('TJ' in message.value['bus_code']):
                async_to_sync(channel_layer.group_send)("events", {"type": "tracking.message","message": message.value})
        except Exception as e:
            print(str(e))

def trip_thread():
    consumer = KafkaConsumer(
        'triptj',
        bootstrap_servers=[settings.KAFKA_PRODUCER_IP+':9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)("events", {"type": "trip.message","message": message.value})
        except Exception as e:
            print(str(e))
        time.sleep(2)

def index(request):
    global trackingThread
    if trackingThread is None:
        thread = Thread(target=tracking_thread)
        thread.daemon = True
        thread.start()

    global tripThread
    if tripThread is None:
        thread = Thread(target=trip_thread)
        thread.daemon = True
        thread.start()

    print(settings.KAFKA_PRODUCER_IP)

    response = {}
    return render(request, 'index.html', response)