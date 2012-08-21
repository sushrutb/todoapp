'''
Created on Aug 21, 2012

@author: sushrut
'''
from django.core.management.base import BaseCommand
from todo.models import Message

class Command(BaseCommand):
    def handle(self, *args, **options):
        run_config()
        
def run_config():
    message_list = Message.objects.all()
    for message in message_list:
        message.message = message.message + ' '
        message.save()