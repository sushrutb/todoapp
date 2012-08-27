'''
Created on Aug 5, 2012

@author: sushrut
'''
from django.db import models
from django import forms
from django.forms.widgets import Textarea, RadioSelect
from django.contrib.auth.models import User 


class AddStatusForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'class':'messageArea','rows':'4',}))
    
    
