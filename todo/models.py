from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=30)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add=True)
    
class Status(models.Model):
    message = models.CharField(max_length=320)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add = True)
    
class Tag(models.Model):
    name = models.CharField(max_length=30)
    status = models.ForeignKey(Status)
    is_primary = models.BooleanField(default = False)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

class Mention(models.Model):
    name = models.CharField(max_length = 30)
    status = models.ForeignKey(Status)
    is_primary = models.BooleanField(default = False)
    last_modified = models.DateTimeField(auto_now = True, auto_now_add = True)
    

