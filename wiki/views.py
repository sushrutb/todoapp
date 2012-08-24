# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from todo.forms import AddStatusForm
from todo.models import Message, Mention, Tag, MessageTag, SystemTagStatus, SystemTag, StatusDO
from project.models import ProjectUser
from django.utils.safestring import mark_safe
from django.db import connection
import re
from todoapp.settings import page_length
from todo.views import process_message_form, get_popular_tags, get_project_list, format_message

@login_required
def show_wiki(request):
    
    #process form
    if request.method == 'POST':
        if request.method == "POST":
            form = AddStatusForm(request.POST)
            if (form.is_valid()):
                process_message_form(request, "/")
                return HttpResponseRedirect(request.path)
            
    main_tag = '#wiki'
    wiki_tag = Tag.objects.filter(user=request.user, name='#wiki')
    message_list = [message_tag.message.message for message_tag in MessageTag.objects.filter(tag=wiki_tag)]
    tag_data = mod_rec_process_messages2(message_list, main_tag)
    print tag_data
    message_tag_list = MessageTag.objects.filter(tag=wiki_tag).exclude(message__status='deleted').order_by('-last_modified')
    
    message_list = [format_message(message_tag.message) for message_tag in message_tag_list]

    return render(request, 'wiki/wiki_view.html', {
        'form': AddStatusForm(),
        'project_list':get_project_list(request.user),
        'popular_tag_list':get_popular_tags(request.user),
        'tag_list':tag_data,
        'message_list':message_list,
    })
    
def process_messages(message_list):
    tag_data = {}
    tag_counters = {}
    final_tags = {}
    for message in message_list:
        tags = re.findall('#(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        if len(tags) == 0:
            continue
        for main_tag in tags:
            if main_tag not in tag_data:
                tag_data[main_tag] = {'total':0, }
            tag_details = tag_data[main_tag]
            tag_details['total'] = tag_details['total'] + 1
            if main_tag not in tag_counters:
                tag_counters[main_tag] = 0
            tag_counters[main_tag] = tag_counters[main_tag] + 1 
            for secondary_tag in tags:
                if secondary_tag == main_tag:
                    continue
                if secondary_tag not in tag_details:
                    tag_details[secondary_tag] = 1
                else:
                    tag_details[secondary_tag] = tag_details[secondary_tag] + 1

    for main_tag in tag_counters.keys():
        tag_details = tag_data[main_tag]
        total = tag_counters[main_tag]
        flag = True
        for sec_tag in tag_details.keys():
            if sec_tag == 'total':
                continue
            if tag_details[sec_tag] >= total:
                flag = False
        final_tags[main_tag] = flag
        
    final_tags1 = {}
    for main_tag in tag_counters.keys():
        tag_details = tag_data[main_tag]
        total = tag_counters[main_tag]
        flag = True
        temp_total = 0
        for sec_tag in tag_details.keys():
            if sec_tag == 'total':
                continue
            if final_tags[sec_tag]:
                temp_total += tag_counters[sec_tag]
        if temp_total >= total:
            final_tags1[main_tag] = False
        else:
            final_tags1[main_tag] = True
    
    return {'final_tags':final_tags1, 'tag_counters':tag_counters}

def strip_message_list(message_list, process_tag):
    new_message_list = []
    for message in message_list:
        if process_tag in message:
            new_message_list.append(message.replace(process_tag,''))
            
    return new_message_list

def filter_message_list(message_list, process_tag):
    new_message_list = []
    for message in message_list:
        if process_tag in message:
            new_message_list.append(message)

    return new_message_list

def mod_rec_process_messages(message_list, process_tag):
    tag_data = []
    
    message_list = filter_message_list(message_list, process_tag)
    message_list = strip_message_list(message_list, process_tag)
    result = process_messages(message_list)
    final_tags = result['final_tags']
    subtags = []
    for final_tag in final_tags.keys():
        if final_tags[final_tag] == True:
            subtags.append(mod_rec_process_messages(message_list, final_tag))
            
    tag_data.append(process_tag)
    if len(subtags) > 0:
        tag_data.append(subtags)
    else:
        return process_tag
    return tag_data

def mod_rec_process_messages2(message_list, process_tag):
    tag_data = []
    
    message_list = filter_message_list(message_list, process_tag)
    message_list = strip_message_list(message_list, process_tag)
    result = process_messages(message_list)
    final_tags = result['final_tags']
    if len(final_tags.keys()) == 0:
        tag_data.append('li')
        tag_data.append(process_tag)
        tag_data.append('/li')
        return tag_data
    tag_data.append('ul')
    tag_data.append('li')
    tag_data.append(process_tag)
    tag_data.append('/li')
    for final_tag in final_tags.keys():
        if final_tags[final_tag] == True:
            subtags = mod_rec_process_messages2(message_list, final_tag)
            tag_data += subtags
    tag_data.append('/ul')
    return tag_data
