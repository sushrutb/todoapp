from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       # shows list of products, ordered by recently added.
                       url(r'^$', 'todo.views.index'),
                       url(r'^wiki/(?P<tag_name>[-\w]+)/$', 'todo.views.get_tag_view'),
                       (r'^accounts/logout/$', logout, {'next_page': '/'}),
                       (r'^accounts/', include('registration.backends.default.urls')),
                       url(r'', include('social_auth.urls')),
)
