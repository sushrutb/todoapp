'''
Created on Aug 13, 2012

@author: sushrut
'''
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'project.views.index'),
    url(r'new/$', 'project.views.add_new'),
    url(r'^(?P<project_name>[-\w]+)/$', 'project.views.project'),
    
)
