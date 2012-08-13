from django.db import models
from django.contrib.auth.models import User
from todo.models import Tag

class Project(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add=True)
    
class ProjectUser(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    role = models.CharField(max_length=16, default='member')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add=True)
    