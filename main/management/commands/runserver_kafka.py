from django.core.management.base import BaseCommand
from django.utils import timezone
from KafkaFinalProject_Consumer import settings
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runserver with custom Kafka IP'

    def add_arguments(self, parser):
        parser.add_argument('ip', type=str, help='Indicates the ip address')

    def handle(self, *args, **kwargs):
        ip = kwargs['ip']
        settings.KAFKA_PRODUCER_IP = ip
        call_command('runserver','0.0.0.0:8000')
        