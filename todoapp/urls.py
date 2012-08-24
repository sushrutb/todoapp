from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings


# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
                       # shows list of products, ordered by recently added.
                       url(r'^$', 'todo.views.index'),
                       url(r'^message/(?P<message_id>[-\w]+)/edit/$', 'todo.views.edit_message'),
                       url(r'^message/new/$', 'todo.views.new_message'),
                       #url(r'^message/(?P<message_id>[-\w]+)/$', 'todo.views.view_message'),
                       url(r'^tag/update', 'todo.views.update_status'),
                       url(r'^tags/$', 'todo.views.get_tags'),
                       url(r'^help/$', 'todo.views.view_help'),
                       url(r'^tag/(?P<tag_name>[-\w]+)/$', 'todo.views.get_tag_view'),
                       url(r'^search/$', 'todo.views.search'),
                       (r'^accounts/logout/$', logout, {'next_page': '/'}),
                       (r'^accounts/', include('registration.backends.default.urls')),
                       url(r'', include('social_auth.urls')),
                       (r'^project/', include('project.urls')),
                       (r'^wiki/', include('wiki.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': settings.STATIC_URL + 'favicon.ico'}),
)
urlpatterns += staticfiles_urlpatterns()
