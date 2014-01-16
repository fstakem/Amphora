# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: user.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 1.7.14
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button

# App imports
from ..models import UserProfile, Project, Analysis, Data, Location, Host
from helper import isUsersPageAndLoggedIn

# Main
user_view_types = {'public': 'public', 'private': 'private'}
user_views = set([ 'activities',
                   'projects_all',
                   'projects_new',
                   'people_following',
                   'people_followers',
                   'people_contributors',
                   'settings_personal',
                   'settings_account'
                    ])

def user(request, user_name):
    view = 'activities'
    view_type = user_view_types['public']
    
    try:
        view_param = request.GET['view']
        if view_param in user_views:
            view = view_param
    except KeyError:
        pass
    
    viewer = request.user
    user_to_be_viewed = list( User.objects.filter(username=user_name) )
    
    if user_to_be_viewed:
        user_to_be_viewed = user_to_be_viewed[0]
        
        if isUsersPageAndLoggedIn(viewer, user_to_be_viewed):
            view_type = user_view_types['private']
        else:
            view_type = user_view_types['public']

        views = view.split('_')
        view_base = views[0]
        sub_view = ''

        if len(views) > 1:
            sub_view = views[1]
        
        if view_base == 'activities':
            return activities(request, user_to_be_viewed, view_type, viewer)

        elif view_base == 'projects':
            return projects(request, sub_view, user_to_be_viewed, view_type, viewer)
        
        elif view_base == 'people':
            return people(request, sub_view, user_to_be_viewed, view_type, viewer)

        elif view_base == 'settings' and view_type == user_view_types['private']:
            return settings(request, sub_view, user_to_be_viewed, view_type, viewer)
        
        else:
            return HttpResponse(status=404)
    
    return HttpResponse(status=404)

def activities(request, user_to_be_viewed, view_type, viewer):
    activities = []



    activity_data = getActivityData(activities)

    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'Activity',
                    'activity_data': activity_data
                }
    
    return render_to_response('./socialnet/user/activities.html', page_data)

def projects(request, sub_view, user_to_be_viewed, view_type, viewer):
    if sub_view == 'new':
        return newProject(request, user_to_be_viewed, view_type, viewer)
    else:
        return allProjects(user_to_be_viewed, view_type, viewer)

def allProjects(user_to_be_viewed, view_type, viewer):
    projects = set(Project.objects.filter(owner__id=user_to_be_viewed.id))
    contrib_projects = list(Project.objects.filter(contributor__id=user_to_be_viewed.id))
    projects.update(contrib_projects)

    projects = list(projects)
    projects.sort(key=lambda x: x.last_activity, reverse=True)
    project_data = getProjectData(projects, user_to_be_viewed)

    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'Projects',
                    'project_data': project_data
                }

    return render_to_response('./socialnet/user/projects.html', page_data)

def newProject(request, user_to_be_viewed, view_type, viewer):
    form = NewProjectForm(request.POST or None)
    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'Projects',
                    'new_project_form': form,
                }

    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)

    
    return render(request, './socialnet/user/new_project.html', page_data)

def people(request, sub_view, user_to_be_viewed, view_type, viewer):
    people = []
    
    if sub_view == 'followers':
        people = User.objects.filter(additional_info__followed__id=user_to_be_viewed.id)
    elif sub_view == 'contributors':
        people = getContributors(user_to_be_viewed)
    else:
        people = User.objects.filter(follower__id=user_to_be_viewed.id)

    people_left, people_right = separateIntoColumns(people, 2)
        
    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'People',
                    'sub_view': sub_view,
                    'people_left': people_left,
                    'people_right': people_right
                }

    return render_to_response('./socialnet/user/people.html', page_data)

def settings(request, sub_view, user_to_be_viewed, view_type, viewer):
    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'Settings',
                    'sub_view': sub_view,
                }
    
    return render_to_response('./socialnet/user/settings.html', page_data)


def getContributors(user_to_be_viewed):
    contributors = set()
    projects = Project.objects.filter(owner__id=user_to_be_viewed.id)

    for project in projects:
        temp_contributors = User.objects.filter(contributed_project__id=project.id)

        for temp in temp_contributors:
            if temp not in contributors and temp != user_to_be_viewed:
                contributors.add(temp)

    contributors = list(contributors)

    return contributors

def separateIntoColumns(people, num_of_cols):
    columns = []

    for i in range(num_of_cols):
        columns.append([])

    if len(people) > 0:
        people = list(people)
        people.sort(key=lambda x: x.username)
        people_data = getPersonalData(people)

        for i, data in enumerate(people_data):
            r = i % num_of_cols
            columns[r].append(data)

    return columns

def getPersonalData(people):
    personal_data = []

    for person in people:
        personal_data.append( [person.username, person.additional_info.title, person.additional_info.profile_photo.url] )

    return personal_data

def getProjectData(projects, user_to_be_viewed):
    project_data = []

    for project in projects:
        last_activity = project.last_activity.strftime("%B %d")
        hosts = len(Host.objects.filter(project__id=project.id))
        data_files = len(Data.objects.filter(project__id=project.id))
        analysis = len(Analysis.objects.filter(project__id=project.id))
        owner = False
        if project.owner.id == user_to_be_viewed.id:
            owner = True
        project_data.append([project.name, last_activity, project.description, project.public, owner, hosts, data_files, analysis])

    return project_data

def getActivityData(activities):
    activity_data = []

    for activity in activities:
        activity_data.append(['Test', 'Test', 'Test', 'Test'])

    return activity_data

class NewProjectForm(forms.Form):
    name = forms.CharField(max_length=200)
    public = forms.BooleanField()
    description = forms.CharField(max_length=400)
    #website = forms.
    #tags = forms.
    
    def __init__(self, *args, **kwargs):
        super(NewProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-project-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_project'
        self.helper.help_text_as_placeholder = True
        
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Button('cancel', 'Cancel'))









