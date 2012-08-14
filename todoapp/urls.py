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

def run_config():
    create_system_tags()
    user_list = User.objects.all()
    for user in user_list:
        print 'user ' + str(user.id) + ' processed'
        
    print 'configs created successfully'
    
def create_system_tags():
    for tag in system_tags.keys():
        print tag
        try:
            system_tag = SystemTag.objects.get(system_tag=tag)
        except SystemTag.DoesNotExist:
            system_tag = SystemTag()
            system_tag.name = tag
            system_tag.save()
        for status in system_tags[tag]:
            try:
                system_tag_status = SystemTagStatus.objects.get(system_tag=system_tag, status=status)
            except SystemTagStatus.DoesNotExist:
                system_tag_status = SystemTagStatus()
                system_tag_status.system_tag = system_tag
                system_tag_status.status = status
                system_tag_status.save()
            print status
            
run_config()