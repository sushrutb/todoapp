# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from forms import AddProjectForm
from models import Project, ProjectUser
from todo.models import Tag
from todo.views import show_index_view


@login_required
def index(request):
    return HttpResponse("In project index view")

@login_required
def project(request, project_name):
    return show_index_view(request, '/project/'+project_name, '#'+project_name)

@login_required
def add_new(request):
    user = request.user
    if request.method == "POST":
        form = AddProjectForm(request.POST)
        if (form.is_valid()):
            name = form.cleaned_data['name']
            project = Project()
            project.name = name
            project.user = user
            project.save()
            
            project_user = ProjectUser()
            project_user.project = project
            project_user.user = user
            project_user.save()
            
            tag = Tag()
            tag.name = '#' + name
            tag.user = user
            tag.type = 'project'
            tag.save()
            return HttpResponseRedirect('/project/' + name)

    return render(request, 'project/add_new.html', {
        'form': AddProjectForm(),
    })
