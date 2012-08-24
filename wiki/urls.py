'''
Created on Aug 24, 2012

@author: sushrut
'''
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'wiki.views.show_wiki'),
    
)
