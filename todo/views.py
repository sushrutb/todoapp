# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from forms import AddStatusForm
from models import Status, Mention, Tag, StatusTag
from django.utils.safestring import mark_safe
import re


@login_required
def index(request):
    user=request.user
    if request.method == "POST":
        form = AddStatusForm(request.POST)
        if (form.is_valid()):
            message = form.cleaned_data['message']
            status = Status(message=message, user=request.user)
            status.save()
            
            # Find and save tags
            tags = re.findall('#(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
            for tag in tags:
                try:
                    new_tag = Tag.objects.get(name=tag, user=user)
                except Tag.DoesNotExist:
                    new_tag = Tag(name=tag, user=user, type='user')
                    new_tag.save()
                status_tag = StatusTag(tag=new_tag, status=status)
                status_tag.save()
            # Find and save mentions
            mentions = re.findall('@(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
            for mention in mentions:
                new_mention = Mention(name=mention, status=status)
                new_mention.save()
            return HttpResponseRedirect("/")

    status_list = Status.objects.filter(user=user).order_by('-last_modified')
    for status in status_list:
        tags = re.findall('#(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', status.message)
        for tag in tags:
            status.message = status.message.replace(tag, '<a href="http://127.0.0.1:8000/tag/' + tag.replace('#', '') + '">' + tag + '</a>')
            mark_safe(status.message)
            print status.message
                
    return render(request, 'todo/index.html', {
        'form': AddStatusForm(),
        'status_list':status_list,
    })

@login_required    
def get_tag_view(request, tag_name):
    user = request.user
    tag = get_object_or_404(Tag, user=user, name='#'+tag_name)
    status_tag_list = StatusTag.objects.filter(tag=tag)
    status_list = Status.objects.filter(user=user, statustag__in = status_tag_list)
    for status in status_list:
        tags = re.findall('#(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', status.message)
        for tag in tags:
            status.message = status.message.replace(tag, '<a href="http://127.0.0.1:8000/tag/' + tag.replace('#', '') + '">' + tag + '</a>')
            mark_safe(status.message)
            print status.message
                
    return render(request, 'todo/index.html', {
        'form': AddStatusForm(),
        'status_list':status_list,
    })
