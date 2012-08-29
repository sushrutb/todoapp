'''
Created on Aug 13, 2012

@author: sushrut
'''
from django import forms


class AddProjectForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput)
    
    
