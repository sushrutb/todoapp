from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from settings import system_tags
from django.contrib.auth.models import User
from todo.models import SystemTag, SystemTagStatus

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       # shows list of products, ordered by recently added.
                       url(r'^$', 'todo.views.index'),
                       url(r'^tag/update', 'todo.views.update_status'),
                       url(r'^tag/(?P<tag_name>[-\w]+)/$', 'todo.views.get_tag_view'),
                       (r'^accounts/logout/$', logout, {'next_page': '/'}),
                       (r'^accounts/', include('registration.backends.default.urls')),
                       url(r'', include('social_auth.urls')),
                       (r'^project/', include('project.urls')),
)

