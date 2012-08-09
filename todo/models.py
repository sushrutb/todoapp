from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from registration.signals import user_activated
from registration.backends.default import DefaultBackend

class Project(models.Model):
    name = models.CharField(max_length=30)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add=True)

class Tag(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User)
    type = models.CharField(max_length=16, default='user')
    last_modified = models.DateTimeField(auto_now = True, auto_now_add = True)
    
class Message(models.Model):
    message = models.CharField(max_length=320)
    user = models.ForeignKey(User)
    status = models.CharField(max_length=30, default='created')
    primary_tag = models.ForeignKey(Tag, null = True)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add = True)
    
class TagStatus(models.Model):
    tag = models.ForeignKey(Tag)
    status = models.CharField(max_length=16, default = 'created')
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

@receiver(user_activated, sender=DefaultBackend)
def user_activated_process(sender, **kwargs):
    user = kwargs.pop('user', None)
    system_tags = [('#expenses', ('reported', 'reimbursed')), ('#buy', ('bought',)),
                   ('#todo', ('completed',)), ('#invoice', ('sent',)), ('#readlater', ('done',)), ('#bookmark',()), ('#diary',()),]
    
    for tag in system_tags:
        new_tag = Tag(user=user, name=tag[0], type='system')
        new_tag.save()
        for status in tag[1]:
            tag_status = TagStatus(tag=new_tag, status=status)
            tag_status.save()