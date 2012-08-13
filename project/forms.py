'''
Created on Aug 13, 2012

@author: sushrut
'''
from django.db import models
from django import forms
from django.forms.widgets import Textarea, RadioSelect
from django.contrib.auth.models import User 


class AddProjectForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput)
    
    
