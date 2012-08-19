from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from forms import AddStatusForm
from models import Message, Mention, Tag, MessageTag, SystemTagStatus, SystemTag, StatusDO
from project.models import ProjectUser
from django.utils.safestring import mark_safe
from django.db import connection
import re

page_length = 5

@login_required
def search(request):
    user = request.user
    page = int(request.GET.get('page', '1'))
    query = request.GET.get('query', None)
    message_list = Message.objects.filter(user=user,message__icontains=query).order_by('-last_modified')[:page_length * page]
    message_list = [format_message(message) for message in message_list]
    project_list = get_project_list(user)
    popular_tag_list = get_popular_tags(user)
    return render(request, 'todo/index.html', {
        'form': AddStatusForm(),
        'message_list':message_list,
        'project_list':project_list,
        'popular_tag_list':popular_tag_list,
        'page':page+1,
    })

@login_required    
def get_tag_view(request, tag_name):
    page = int(request.GET.get('page', '1'))
    tag = Tag.objects.get(user=request.user, name='#'+tag_name)
    user=request.user
    process_form(request)
    message_tag_list = MessageTag.objects.filter(tag=tag).exclude(message__status='deleted').order_by('-last_modified')[:5 * page]
    
    message_list = [format_message(message_tag.message) for message_tag in message_tag_list]
    form = AddStatusForm(initial={'message':'#'+tag_name + ' '})
    project_list = get_project_list(user)
    popular_tag_list = get_popular_tags(user)
    return render(request, 'todo/index.html', {
        'form': form,
        'message_list':message_list,
        'project_list':project_list,
        'popular_tag_list':popular_tag_list,
        'page':page+1,
    })

       
@login_required
def index(request):
    page = int(request.GET.get('page', '1'))
    user=request.user
    process_form(request)
    message_list = [format_message(message) for message in Message.objects.filter(user=user).exclude(status='deleted').order_by('-last_modified')[:5 * page]]
    project_list = get_project_list(user)
    popular_tag_list = get_popular_tags(user)
    return render(request, 'todo/index.html', {
        'form': AddStatusForm(),
        'message_list':message_list,
        'project_list':project_list,
        'popular_tag_list':popular_tag_list,
        'page':page+1,
    })
    
@login_required
def update_status(request):
    message_id = request.GET.get('message_id', '')
    new_status = request.GET.get('new_status', '')
    
    
    message = Message.objects.get(id=message_id)
    message.status = new_status
    message.save()
    return HttpResponseRedirect(request.path)

def format_message(message):
    status_do = StatusDO()
    primary_tag = message.primary_tag
    if primary_tag is not None and primary_tag.type == 'system':
        
        status_do.tag_id = primary_tag.id
        tag_status_list = SystemTagStatus.objects.filter(system_tag=SystemTag.objects.get(system_tag=primary_tag.name))
        for tag_status in tag_status_list:
            if tag_status.status != message.status:
                status_do.links.append(tag_status.status)
            else:
                status_do.links = []

    status_do.id = message.id
    message_tags = MessageTag.objects.filter(message=message)
    status_do.message = message.message
    for message_tag in message_tags:
        status_do.message = status_do.message.replace(message_tag.tag.name, '<a href="/tag/' + message_tag.tag.name.replace('#', '') + '">' + message_tag.tag.name + '</a>')
        mark_safe(status_do.message)
        
    return status_do

def show_index_view(request, redirecturl, tag_name):
    user=request.user
    
    # process form if the request is POST
    if request.method == "POST":
        form = AddStatusForm(request.POST)
        if (form.is_valid()):
            return process_message_form(request, redirecturl, tag_name)
    
    # Get status and format them
    if tag_name is None:    
        message_list = [format_message(message) for message in Message.objects.filter(user=user).exclude(status='deleted').order_by('-last_modified')]
        form = AddStatusForm()
    else:
        tag = Tag.objects.get(user=user, name=tag_name)
        message_list = [format_message(message_tag.message) for message_tag in MessageTag.objects.filter(tag=tag).exclude(message__status='deleted').order_by('-last_modified')]
        form = AddStatusForm(initial={'message':tag_name + ' '})
    
    project_list = get_project_list(user)
    popular_tag_list = get_popular_tags(user)
    return render(request, 'todo/index.html', {
        'form': form,
        'message_list':message_list,
        'project_list':project_list,
        'popular_tag_list':popular_tag_list,
    })

def process_message_form(request, redirecturl):
    form = AddStatusForm(request.POST)
    user = request.user
    
    if (form.is_valid()):
        message_ = form.cleaned_data['message']
    
    # Find all hashtags.
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
        
    process_tags(tags, message, user)
    process_mentions(message)
        

def process_mentions(message):
    mentions = re.findall('@(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.message)
    for mention in mentions:
        new_mention = Mention(name=mention, message=message)
        new_mention.save()
    
def process_tags(tags, message, user):
    for tag in tags:
        try:
            new_tag = Tag.objects.get(name=tag, user=user)
        except Tag.DoesNotExist:
            new_tag = Tag(name=tag, user=user, type='user')
            new_tag.save()
        message_tag = MessageTag(tag=new_tag, message=message)
        message_tag.save()
        
def get_project_list(user):
    project_list = [project_user.project for project_user in ProjectUser.objects.filter(user=user, project__status='active')]
    return project_list

def get_popular_tags(user):
    cursor = connection.cursor()
    cursor.execute("select name from todo_tag where todo_tag.id in (select primary_tag_id from todo_message where user_id = %s and primary_tag_id not in (select id from todo_tag where user_id = %s and type='project') group by primary_tag_id order by count(*) desc)",[user.id, user.id])
    tags = cursor.fetchall()
    tags = [tag[0].replace('#','') for tag in tags]
    return tags

def process_form(request):
    # process form if the request is POST
    if request.method == "POST":
        form = AddStatusForm(request.POST)
        if (form.is_valid()):
            process_message_form(request, request.path)
            return HttpResponseRedirect(request.path)
