from django.db import models
from django.db.models import signals
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver 
from todo.models import Tag

class Project(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30, default = 'misc')
    status = models.CharField(max_length=30, default='active')
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add=True)
    
class ProjectUser(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    role = models.CharField(max_length=16, default='member')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add=True)

@receiver(post_save, sender=Project)
def project_created(sender, **kwargs):
    created = kwargs.pop('created', True)
    if created == True:
        project_tags = [('#todo', ('completed',)), ('#invoice', ('sent',)), ('#readlater', ('done',)), ('#bookmark',()), ('#diary',()),]