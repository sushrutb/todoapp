# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from forms import AddStatusForm
from models import Message, Mention, Tag, MessageTag, TagStatus, StatusDO
from django.utils.safestring import mark_safe
import re


@login_required
def index(request):
    return show_index_view(request, "/", None)
    
@login_required
def update_status(request):
    tag_id = request.GET.get('tag_id', '')
    message_id = request.GET.get('message_id', '')
    new_status = request.GET.get('new_status', '')
    
    tag = Tag.objects.get(id=tag_id)
    message = Message.objects.get(id=message_id)
    message_tag = MessageTag.objects.get(tag=tag, message=message)
    message_tag.status = new_status
    message_tag.save()
    #print 'status updated ' + message_tag.st
    return HttpResponseRedirect("/")

def format_message(message):
    status_do = StatusDO()
    status_do.id = message.id
    message_tags = MessageTag.objects.filter(message=message)
    for message_tag in message_tags:
        status_do.message = message.message.replace(message_tag.tag.name, '<a href="http://127.0.0.1:8000/tag/' + message_tag.tag.name.replace('#', '') + '">' + message_tag.tag.name + '</a>')
        mark_safe(status_do.message)
        status_do.tag_id = message_tag.tag.id
        tag_status_list = TagStatus.objects.filter(tag=message_tag.tag)
        for tag_status in tag_status_list:
            if tag_status.status != message_tag.status:
                status_do.links.append(tag_status.status)
            else:
                status_do.links = []
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
            message = Message(message=message_, user=request.user)
            message.save()
            
            # Find and save tags
            tags = re.findall('#(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.message)
            for tag in tags:
                try:
                    new_tag = Tag.objects.get(name=tag, user=user)
                except Tag.DoesNotExist:
                    new_tag = Tag(name=tag, user=user, type='user')
                    new_tag.save()
                message_tag = MessageTag(tag=new_tag, message=message, status='created')
                message_tag.save()
            # Find and save mentions
            mentions = re.findall('@(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.message)
            for mention in mentions:
                new_mention = Mention(name=mention, message=message)
                new_mention.save()
            return HttpResponseRedirect(redirecturl)
    
    if tag_name is None:    
        message_list = [format_message(message) for message in Message.objects.filter(user=user).order_by('-last_modified')]
    else:
        tag = Tag.objects.get(user=user, name=tag_name)
        message_list = [format_message(message_tag.message) for message_tag in MessageTag.objects.filter(tag=tag).order_by('-last_modified')]
    
    return render(request, 'todo/index.html', {
        'form': AddStatusForm(),
        'message_list':message_list,
    })
