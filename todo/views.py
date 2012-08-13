# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django import forms
from django.forms import widgets
from forms import AddStatusForm
from models import Message, Mention, Tag, MessageTag, TagStatus, StatusDO
from django.utils.safestring import mark_safe
import re


@login_required
def index(request):
    return show_index_view(request, "/", None)
    
@login_required
def update_status(request):
    message_id = request.GET.get('message_id', '')
    new_status = request.GET.get('new_status', '')
    
    
    message = Message.objects.get(id=message_id)
    message.status = new_status
    message.save()
    return HttpResponseRedirect("/")

def format_message(message):
    status_do = StatusDO()
    primary_tag = message.primary_tag
    if primary_tag is not None:
        status_do.tag_id = primary_tag.id
        tag_status_list = TagStatus.objects.filter(tag=primary_tag)
        for tag_status in tag_status_list:
            if tag_status.status != message.status:
                status_do.links.append(tag_status.status)
            else:
                status_do.links = []
        
    status_do.id = message.id
    message_tags = MessageTag.objects.filter(message=message)
    for message_tag in message_tags:
        status_do.message = message.message.replace(message_tag.tag.name, '<a href="http://127.0.0.1:8000/tag/' + message_tag.tag.name.replace('#', '') + '">' + message_tag.tag.name + '</a>')
        mark_safe(status_do.message)
        
    return status_do

@login_required    
def get_tag_view(request, tag_name):
    return show_index_view(request, "/tag/"+tag_name, '#'+tag_name)

def show_index_view(request, redirecturl, tag_name):
    user=request.user
    if request.method == "POST":
        form = AddStatusForm(request.POST)
        if (form.is_valid()):
            message_ = form.cleaned_data['message']
            
            # Find and save tags
            tags = re.findall('#(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message_)
            
            #Save message with primary tag
            primary_tag = None
            if tags is not None and len(tags)>0:
                primary_tag_name = tags[0]
                try:
                    primary_tag = Tag.objects.get(name=primary_tag_name, user=user)
                except Tag.DoesNotExist:
                    primary_tag = Tag(name=primary_tag_name, user=user, type='user')
                    primary_tag.save()
                    
            message = Message(message=message_, user=request.user)
            message.primary_tag = primary_tag
            message.save()
                
            for tag in tags:
                try:
                    new_tag = Tag.objects.get(name=tag, user=user)
                except Tag.DoesNotExist:
                    new_tag = Tag(name=tag, user=user, type='user')
                    new_tag.save()
                message_tag = MessageTag(tag=new_tag, message=message)
                message_tag.save()
                
            # Find and save mentions
            mentions = re.findall('@(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.message)
            for mention in mentions:
                new_mention = Mention(name=mention, message=message)
                new_mention.save()
            return HttpResponseRedirect(redirecturl)
    
    if tag_name is None:    
        message_list = [format_message(message) for message in Message.objects.filter(user=user).exclude(status='deleted').order_by('-last_modified')]
        form = AddStatusForm()
    else:
        tag = Tag.objects.get(user=user, name=tag_name)
        message_list = [format_message(message_tag.message) for message_tag in MessageTag.objects.filter(tag=tag).exclude(message__status='deleted').order_by('-last_modified')]
        form = AddStatusForm(initial={'message':tag_name + ' '})
    
    
    
    return render(request, 'todo/index.html', {
        'form': form,
        'message_list':message_list,
    })