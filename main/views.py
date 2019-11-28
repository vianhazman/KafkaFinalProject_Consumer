from django.shortcuts import render
from threading import Thread
import websocket
from websocket import create_connection
import time, json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from kafka import KafkaConsumer
from json import loads

trackingThread = None
tripThread = None

def tracking_thread():
    consumer = KafkaConsumer(
        'trackingtj',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)("events", {"type": "tracking.message","message": message.value})
        except Exception as e:
            print(str(e))
        time.sleep(2)

def trip_thread():
    consumer = KafkaConsumer(
        'triptj',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
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

    response = {}
    return render(request, 'index.html', response)