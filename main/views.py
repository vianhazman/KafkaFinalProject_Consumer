from django.shortcuts import render
from threading import Thread
import websocket
from websocket import create_connection
import time, json
from main.models import Bus, GpsPing
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from kafka import KafkaConsumer
from json import loads
from KafkaFinalProject_Consumer import settings
import queue
import time


trackingThread = None
tripThread = None
queueThread = None
bus_code = "MYS"
obj_queue = queue.Queue() 

def put_queue_thread(obj):
    obj_queue.put(obj)
    
def save_queue_thread():
    while True:
        if (obj_queue.qsize() != 0):
            obj = obj_queue.get()
            obj.save()
            print("[STORE] " + str(obj))


def storing_thread1(msg):
    try:
        buscode = msg['bus_code']
        trip_id = msg['trip_id']
        koridor = msg['koridor']
        timestamp = msg['timestamp']
        bus = Bus.create(buscode, trip_id, koridor, timestamp)
        thread = Thread(target=put_queue_thread,args=(bus,))
        thread.start()
    except Exception as e:
        print(str(e))

def storing_thread2(message):
    msg = message.value
    try:
        buscode = msg['bus_code']
        trip_id = msg['latitude']
        koridor = msg['longitude']
        timestamp = msg['gps_timestamp']
        ping = GpsPing.create(buscode, trip_id, koridor, timestamp)
        thread = Thread(target=put_queue_thread,args=(ping,))
        thread.start()
    except Exception as e:
        print(str(e))


def tracking_thread():
    consumer = KafkaConsumer(
        'trackingtj',
        bootstrap_servers=[settings.KAFKA_PRODUCER_IP+':9092'],
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    consumer.poll()
    #go to end of the stream
    consumer.seek_to_end()
    for message in consumer:
        print("[VIZ] "+str(message.value))
        try:
            channel_layer = get_channel_layer()
            if (bus_code in message.value['bus_code']):
                #send data ke front end via websocket
                async_to_sync(channel_layer.group_send)("events", {"type": "tracking.message","message": message.value})
            #trigger storing thread untuk melakukan penyimpanan data ke data warehouse
            thread = Thread(target=storing_thread2,args=(message,))
            thread.start()
        except Exception as e:
            print(str(e))

def trip_thread():
    consumer = KafkaConsumer(
        'pg1.public.trips',
        bootstrap_servers=[settings.KAFKA_PRODUCER_IP+':9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        try:
            msg = message.value['payload']['after']
            print("[VIZ] "+str(msg))
            channel_layer = get_channel_layer()
            
            #send data ke front end via websocket
            async_to_sync(channel_layer.group_send)("events", {"type": "trip.message","message": msg})

            #trigger storing thread untuk melakukan penyimpanan data ke data warehouse
            thread = Thread(target=storing_thread1,args=(msg,))
            thread.start()
        except Exception as e:
            print(str(e))
        time.sleep(2)

def index(request):

    global obj_queue

    global bus_code
    bus_code = request.GET['bus_code']
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

    global queueThread
    if queueThread is None:
        thread = Thread(target=save_queue_thread)
        thread.daemon = True
        thread.start()

    print(settings.KAFKA_PRODUCER_IP)

    response = {"bus_code":bus_code}
    return render(request, 'index.html', response)