# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


class VisualizationCustomer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)('events', self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("events", self.channel_name)
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    def trip_message(self, text_data):
        text_data_json = text_data
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'type':'trip',
            'message': message
        }))

    def tracking_message(self, text_data):
        text_data_json = text_data
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'type':'tracking',
            'message': message
        }))

    
