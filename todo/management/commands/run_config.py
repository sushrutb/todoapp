from todoapp.settings import system_tags
from django.contrib.auth.models import User
from todo.models import SystemTag, SystemTagStatus, Tag
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.dispatch import receiver
from registration.signals import user_activated
from registration.backends.default import DefaultBackend

class Command(BaseCommand):
    def handle(self, *args, **options):
        run_config()
        
def run_config():
    create_system_tags()
    user_list = User.objects.all()
    for user in user_list:
        run_user_config(user)
        
    print 'configs created successfully'
    
def run_user_config(user):
    for tag in system_tags.keys():
        try:
            user_tag = Tag.objects.get(user=user, name=tag)
            user_tag.type = 'system'
            user_tag.save()
        except Tag.DoesNotExist:
            user_tag = Tag()
            user_tag.name = tag
            user_tag.user = user
            user_tag.type = 'system'
            user_tag.save()
        
    print 'user ' + str(user.id) + ' processed'
    
def create_system_tags():
    for tag in system_tags.keys():
        print tag
        try:
            system_tag = SystemTag.objects.get(system_tag=tag)
        except SystemTag.DoesNotExist:
            system_tag = SystemTag()
            system_tag.system_tag = tag
            system_tag.save()
        if system_tags[tag] is not None:
            for status in system_tags[tag]:
                try:
                    system_tag_status = SystemTagStatus.objects.get(system_tag=system_tag, status=status)
                except SystemTagStatus.DoesNotExist:
                    system_tag_status = SystemTagStatus()
                    system_tag_status.system_tag = system_tag
                    system_tag_status.status = status
                    system_tag_status.save()
                print status
            
