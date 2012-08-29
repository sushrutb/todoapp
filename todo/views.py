from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from forms import AddStatusForm
from models import Message, Mention, Tag, MessageTag, SystemTagStatus, SystemTag, StatusDO
from project.models import ProjectUser
from django.utils.safestring import mark_safe
from django.db import connection
import re
from todoapp.settings import page_length
import urllib2
from bs4 import BeautifulSoup


@login_required
def new_message(request):
    
    if request.method == "POST":
        form = AddStatusForm(request.POST)
        if (form.is_valid()):
            process_message_form(request, "/")
            return HttpResponseRedirect(request.GET.get('url','/'))
    initial_str = '#'+request.GET.get('tag','bookmark ')+' ' + request.GET.get('url','')
    hashtags = process_url(request.GET.get('url',''))
    initial_str += ' ' + hashtags
    form = AddStatusForm(initial={'message': initial_str})    
    return render(request, 'todo/new_message.html', {
        'form': form,
    })
    
def process_url(url):
    if url == '':
        return ''
    if 'stackoverflow.com' not in url:
        return ''
    
    html = urllib2.urlopen(url)
    input_html = html.read()
    soup = BeautifulSoup(input_html)
    
    #tag_list = soup.find_all('/questions/tagged/')
    tag_list = soup.find_all("div",class_='post-taglist')
    post_taglist = tag_list[0]
    links = post_taglist.find_all("a")
    hashtags = ''
    for link_ in links:
        hashtags += ' #' + link_.text
    return hashtags
    
def view_help(request):
    return render(request, 'help.html', {})

def view_introduction(request):
    return render(request, 'introduction.html', {})
    
@login_required
def edit_message(request, message_id):
    user = request.user
    message = get_object_or_404(Message, pk=long(message_id))
    next_page = request.GET.get('next', '/')
    if request.method == "POST":
        form = AddStatusForm(request.POST)
        if (form.is_valid()):
            MessageTag.objects.filter(message=message).delete()
            message.delete()
            process_message_form(request, "/")
            return HttpResponseRedirect(next_page)

    project_list = get_project_list(user)
    popular_tag_list = get_popular_tags(user)
    form = AddStatusForm(initial={'message': message.message})
    
    return render(request, 'todo/edit_message.html', {
        'form': form,
        'project_list':project_list,
        'popular_tag_list':popular_tag_list,
    })
    
@login_required
def get_tags(request):
    user = request.user
    if request.method == 'POST':
        return process_form(request)
    tag_list = Tag.objects.filter(user=user).order_by('name')
    tag_list = [(tag.name.replace('#', ''),) for tag in tag_list]
    project_list = get_project_list(user)
    popular_tag_list = get_popular_tags(user)
    return render(request, 'todo/tags.html', {
        'form': AddStatusForm(),
        'project_list':project_list,
        'popular_tag_list':popular_tag_list,
        'tag_list':tag_list,
    })

@login_required
def search(request):
    user = request.user
    page = int(request.GET.get('page', '1'))
    query = request.GET.get('query', None)
    message_list = Message.objects.filter(user=user, message__icontains=query).order_by('-last_modified')[:page_length * page]
    message_list = [format_message(message) for message in message_list]
    project_list = get_project_list(user)
    popular_tag_list = get_popular_tags(user)
    return render(request, 'todo/index.html', {
        'form': AddStatusForm(),
        'message_list':message_list,
        'project_list':project_list,
        'popular_tag_list':popular_tag_list,
        'page':page + 1,
    })

@login_required    
def get_tag_view(request, tag_name):
    tag_name = '#'+tag_name
    page = int(request.GET.get('page', '1'))
    tag = Tag.objects.get(user=request.user, name=tag_name)
    user = request.user
    if request.method == 'POST':
        return process_form(request)
    message_tag_list = MessageTag.objects.filter(tag=tag).exclude(message__status='deleted').order_by('-last_modified')[:page_length * page]
    
    message_list = [format_message(message_tag.message) for message_tag in message_tag_list]
    form = AddStatusForm(initial={'message':tag_name + ' '})
    project_list = get_project_list(user)
    popular_tag_list = get_popular_tags(user)
    
    if MessageTag.objects.filter(tag=tag).exclude(message__status='deleted').count()>page_length*page:
        last_page = False
    else:
        last_page=True
        
    return render(request, 'todo/index.html', {
        'form': form,
        'message_list':message_list,
        'project_list':project_list,
        'popular_tag_list':popular_tag_list,
        'page':page + 1,
        'last_page':last_page,
        'tag_name':tag_name.replace('#',''),
    })

       
@login_required
def index(request):
    page = int(request.GET.get('page', '1'))
    user = request.user
    if request.method == 'POST':
        return process_form(request)
    message_list = [format_message(message) for message in Message.objects.filter(user=user).exclude(status='deleted').order_by('-last_modified')[:page_length * page]]
    project_list = get_project_list(user)
    popular_tag_list = get_popular_tags(user)
    
    if Message.objects.filter(user=user).exclude(status='deleted').count() > (page_length * page):
        last_page = False
    else:
        last_page = True

    return render(request, 'todo/index.html', {
        'form': AddStatusForm(),
        'message_list':message_list,
        'project_list':project_list,
        'popular_tag_list':popular_tag_list,
        'page':page + 1,
        'last_page':last_page,
    })
    
@login_required
def update_status(request):
    message_id = request.GET.get('message_id', 1)
    new_status = request.GET.get('new_status', '')
    next_page = request.GET.get('next', '/')
    
    message = Message.objects.get(id=long(message_id))
    message.status = new_status
    message.save()
    return HttpResponseRedirect(next_page)

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
    status_do.message  = message.message + ''
    flag = False
    for message_tag in message_tags:
        if message_tag.tag.name == '#imp':
            flag = True
        status_do.message = re.sub(' #(?:' + message_tag.tag.name.replace('#','')+')\\b|\\A#(?:' + message_tag.tag.name.replace('#','') + ')\\b', 
                                   ' <a href="/tag/' + message_tag.tag.name.replace('#', '') + '">' + message_tag.tag.name + '</a>' + '',
                                   status_do.message)
        mark_safe(status_do.message)
    status_do.message = status_do.message.strip()
    status_do.i = flag
    return status_do

def process_message_form(request, redirecturl):
    form = AddStatusForm(request.POST)
    user = request.user
    
    if (form.is_valid()):
        message_ = form.cleaned_data['message']
        #message_ = message_ + ' '
    
    # Find all hashtags.
    #tags = re.findall('#(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message_)
    
    tags = re.findall(r' #(?:[a-zA-Z]|[-])+\b|\A#(?:[a-zA-Z]|[-])+\b', message_)
    tags = [tag_.strip() for tag_ in tags]

    #Save message with primary tag
    primary_tag = None
    if tags is not None and len(tags) > 0:
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
    cursor.execute("select name from todo_tag where todo_tag.id in (select primary_tag_id from todo_message where user_id = %s and primary_tag_id not in (select id from todo_tag where user_id = %s and type='project') group by primary_tag_id order by count(*) desc)", [user.id, user.id])
    tags = cursor.fetchall()
    tags = [tag[0].replace('#', '') for tag in tags]
    return tags

def process_form(request):
    # process form if the request is POST
    if request.method == "POST":
        form = AddStatusForm(request.POST)
        if (form.is_valid()):
            process_message_form(request, request.path)
            return HttpResponseRedirect(request.get_full_path())
