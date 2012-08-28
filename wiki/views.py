# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from todo.forms import AddStatusForm
from todo.models import Tag, MessageTag, Message
import re
from todoapp.settings import page_length
from todo.views import process_message_form, get_popular_tags, get_project_list, format_message, process_form
from django.db import connection

@login_required
def show_wiki(request):
    return show_wiki_view(request, 'wiki')
    
@login_required
def show_wiki_view(request, tag_name):
    tag_name = '#'+tag_name
    page = int(request.GET.get('page', '1'))
    
    if request.method == 'POST':
        return process_form(request)

            
    
    main_tag = Tag.objects.get(user=request.user, name=tag_name)

    message_list = [message_tag.message.message for message_tag in MessageTag.objects.filter(tag=main_tag).exclude(message__status='deleted')]
    tag_data = mod_rec_process_messages2(message_list, tag_name)
    tag_data = tag_data[4:len(tag_data)-2]
    
    tag_data = add_links(tag_data)
    
    message_tag_list = MessageTag.objects.filter(tag=main_tag).exclude(message__status='deleted').order_by('-last_modified')[:page_length * page]
    message_list = [format_message(message_tag.message) for message_tag in message_tag_list]
    
    
    filter_tags = request.GET.getlist('tag')
    if filter_tags is not None and len(filter_tags)>0:
        cursor = connection.cursor()
        cursor.execute("select message_id from todo_messagetag where tag_id = %s", main_tag.id)
        message_id_list = set(cursor.fetchall())
        
        for filter_tag in filter_tags:
            filter_tag = Tag.objects.get(name='#'+filter_tag, user=request.user)
            cursor = connection.cursor()
            cursor.execute("select message_id from todo_messagetag where tag_id = %s", filter_tag.id)
            message_ids = set(cursor.fetchall())
            message_id_list = message_id_list.intersection(message_ids)
            
        message_id_list = [id_[0] for id_ in message_id_list]
            
        message_list = Message.objects.filter(id__in=message_id_list).exclude(status='deleted').order_by('-last_modified')[:page_length * page]
        message_list = [format_message(message) for message in message_list]
        if Message.objects.filter(id__in=message_id_list).exclude(status='deleted').order_by('-last_modified').count() > page_length*page:
            last_page = False
        else:
            last_page = True
    else:
        if MessageTag.objects.filter(tag=main_tag).exclude(message__status='deleted').count() > page_length*page:
            last_page = False
        else:
            last_page = True

    return render(request, 'wiki/wiki_view.html', {
        'form': AddStatusForm(initial={'message': tag_name + ' '}),
        'project_list':get_project_list(request.user),
        'popular_tag_list':get_popular_tags(request.user),
        'tag_list':tag_data,
        'message_list':message_list,
        'last_page':last_page,
        'main_tag':tag_name.replace('#',''),
        'base_url':'/wiki_view/'+tag_name.replace('#',''),
    })
    
def add_links(tag_data):
    new_tag_data = []
    curr_link = ''
    links = []
    for tag_ in tag_data:
        tuple_data = [tag_]
        if tag_ == 'ul':
            links.append(curr_link)
            new_tag_data.append(tuple_data)
        elif tag_ == '/ul':
            links = links[:len(links)-1]
            new_tag_data.append(tuple_data)
        elif tag_ == 'li':
            new_tag_data.append(tuple_data)
        elif tag_ == '/li':
            new_tag_data.append(tuple_data)
        else:
            curr_link = tag_.replace('#','')
            if len(links) > 0:
                link_str = ''
                for link_ in links:
                    link_str += '&tag=' + link_
                tuple_data.append(link_str+'&tag='+curr_link)
            else:
                tuple_data.append('&tag='+curr_link)
            new_tag_data.append(tuple_data)
        
    return new_tag_data 
        
def process_messages(message_list):
    tag_data = {}
    tag_counters = {}
    final_tags = {}
    for message in message_list:
        tags = re.findall(r' #\w+|\A#\w+', message)
        tags = [tag_.strip() for tag_ in tags]
        #tags = re.findall('#(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
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
        #if process_tag in message:
        new_message_list.append(message)

    return new_message_list

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
    tag_data.append('li')
    tag_data.append(process_tag)
    tag_data.append('/li')
    tag_data.append('ul')
    for final_tag in final_tags.keys():
        if final_tags[final_tag] == True:
            subtags = mod_rec_process_messages2(message_list, final_tag)
            tag_data += subtags
    tag_data.append('/ul')
    return tag_data
