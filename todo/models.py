from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from registration.signals import user_activated
from registration.backends.default import DefaultBackend
from datetime import datetime

class Tag(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User)
    type = models.CharField(max_length=16, default='user')
    created = models.DateTimeField(default=datetime.now)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add = True)
    
class Message(models.Model):
    message = models.CharField(max_length=320)
    user = models.ForeignKey(User)
    status = models.CharField(max_length=30, default='created')
    primary_tag = models.ForeignKey(Tag, null = True)
    created = models.DateTimeField(default=datetime.now)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

class Mention(models.Model):
    name = models.CharField(max_length = 30)
    message = models.ForeignKey(Message)
    is_primary = models.BooleanField(default = False)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add = True)
    
class MessageTag(models.Model):
    tag = models.ForeignKey(Tag)
    message = models.ForeignKey(Message)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add = True)
    
class StatusDO:
    def __init__(self):
        self.message = None
        self.links = []
        self.id = None
        self.tag_id = None

class SystemTag(models.Model):
    system_tag = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified= models.DateTimeField(auto_now=True)
    
class SystemTagStatus(models.Model):
    system_tag = models.ForeignKey(SystemTag)
    status = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified= models.DateTimeField(auto_now=True)

@receiver(user_activated, sender=DefaultBackend)
def user_activated_process(sender, **kwargs):
    from management.commands.run_config import run_user_config
    user = kwargs.pop('user', None)
    print 'activating user ' + str(user.id)
    run_user_config(user)
