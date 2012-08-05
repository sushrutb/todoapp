# Create your views here.
from array import *
from django.shortcuts import render, get_object_or_404
from forms import AddStatusForm
from models import Status, Mention, Tag
import logging
import math
import re


def index(request):
    if request.method == "POST":
        form = AddStatusForm(request.POST)
        if (form.is_valid()):
            message = form.cleaned_data['message']
            status = Status(message=message)
            status.save()
            
            # Find and save tags
            tags = re.findall('#(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
            for tag in tags:
                new_tag = Tag(name=tag, status=status)
                new_tag.save()
                
            # Find and save mentions
            mentions = re.findall('@(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
            for mention in mentions:
                new_mention = Mention(name=mention, status=status)
                new_mention.save()
                
    return render(request, 'todo/index.html', {
        'form': AddStatusForm()
    })
    
def get_tag_view(request, tag_name):
    return render(request, 'category/shootout.html', {
        'form': AddStatusForm()
    })
