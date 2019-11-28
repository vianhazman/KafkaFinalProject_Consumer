from django.shortcuts import render
from threading import Thread
import websocket
from websocket import create_connection
import time, json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from kafka import KafkaConsumer
from json import loads

thread = None

def background_thread():
    consumer = KafkaConsumer(
        'test12',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)("events", {"type": "chat.message","message": message.value})
        except Exception as e:
            print(str(e))
        time.sleep(2)

def index(request):
    print(request.get_host())
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()

    response = {}
    return render(request, 'index.html', response)