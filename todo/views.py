# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from forms import AddStatusForm
from models import Status, Mention, Tag, StatusTag, TagStatus, StatusDO
from django.utils.safestring import mark_safe
import re


@login_required
def index(request):
    return show_index_view(request, "/")
    
@login_required
def update_status(request):
    tag_id = request.GET.get('tag_id', '')
    status_id = request.GET.get('status_id', '')
    new_status = request.GET.get('new_status', '')
    
    tag = Tag.objects.get(id=tag_id)
    status = Status.objects.get(id=status_id)
    status_tag = StatusTag.objects.get(tag=tag, status=status)
    status_tag.status_ind = new_status
    status_tag.save()
    return HttpResponseRedirect("/")

def format_status(status):
    status_do = StatusDO()
    status_do.id = status.id
    status_tags = StatusTag.objects.filter(status=status)
    for status_tag in status_tags:
        status_do.message = status.message.replace(status_tag.tag.name, '<a href="http://127.0.0.1:8000/tag/' + status_tag.tag.name.replace('#', '') + '">' + status_tag.tag.name + '</a>')
        mark_safe(status_do.message)
        status_do.tag_id = status_tag.tag.id
        tag_status_list = TagStatus.objects.filter(tag=status_tag.tag)
        for tag_status in tag_status_list:
            print tag_status.status + '========' + status_tag.status_ind
            print tag_status.status != status_tag.status_ind
            if tag_status.status != status_tag.status_ind:
                status_do.links.append(tag_status.status)
            else:
                status_do.links = []
    return status_do

@login_required    
def get_tag_view(request, tag_name):
    return show_index_view(request, "/tag/"+tag_name)

def show_index_view(request, redirecturl):
    #import pdb; pdb.set_trace()
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
                status_tag = StatusTag(tag=new_tag, status=status, status_ind='created')
                status_tag.save()
            # Find and save mentions
            mentions = re.findall('@(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
            for mention in mentions:
                new_mention = Mention(name=mention, status=status)
                new_mention.save()
            return HttpResponseRedirect(redirecturl)
        
    status_list = [format_status(status) for status in Status.objects.filter(user=user).order_by('-last_modified')]
    
    return render(request, 'todo/index.html', {
        'form': AddStatusForm(),
        'status_list':status_list,
    })
