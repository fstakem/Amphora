# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: user.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 12.5.13
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from collections import Set

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils import simplejson
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# App imports
from ..models import UserProfile, Project, Analysis, Data, Revision, Location, Host, SoftwareStack, Version
from helper import isUsersPageAndLoggedIn

# Main
user_view_types = {'public': 'public', 'private': 'private'}
user_views = set([ 'info',
                   'activity',
                   'new_project',
                   'projects',
                   'friends',
                   'contributors',
                   'new_data',
                   'data',
                   'analysis',
                   'new_analysis',
                   'settings' ])

def user(request, user_name):
    view = 'activity'
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
        
        if view == 'info':
            return userInfo(user_to_be_viewed, view_type, viewer)
        
        elif view == 'activity':
            return userActivity(user_to_be_viewed, view_type, viewer)
        
        elif view == 'new_project' and view_type == user_view_types['private']:
            return userNewProject(request, user_to_be_viewed, view_type, viewer)
        
        elif view == 'projects':
            return userProjects(user_to_be_viewed, view_type, viewer)
        
        elif view == 'friends':
            return userFriends(user_to_be_viewed, view_type, viewer)
        
        elif view == 'contributors' and view_type == user_view_types['private']:
            return userContributors(user_to_be_viewed, view_type, viewer)
        
        elif view == 'new_data' and view_type == user_view_types['private']:
            return userNewData(request, user_to_be_viewed, view_type, viewer)
        
        elif view == 'data':
            return userData(user_to_be_viewed, view_type, viewer)
        
        elif view == 'new_analysis' and view_type == user_view_types['private']:
            return userNewAnalysis(request, user_to_be_viewed, view_type, viewer)
        
        elif view == 'analysis':
            return userAnalysis(user_to_be_viewed, view_type, viewer)
        
        elif view == 'settings' and view_type == user_view_types['private']:
            return userSettings(user_to_be_viewed, view_type, viewer)
        
        else:
            return HttpResponse(status=404)
    
    return HttpResponse(status=404)

def userInfo(user_to_be_viewed, view_type, viewer):
    data = { 'user_name': user_to_be_viewed.username,
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'view': 'Info' }
    
    if view_type == user_view_types['private']:
        pass
    elif view_type == user_view_types['public']:
        pass
    
    return render_to_response('./socialnet/user/info.html', data)

def userActivity(user_to_be_viewed, view_type, viewer):
    data = { 'user_name': user_to_be_viewed.username,
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'view': 'Activity' }
    
    if view_type == user_view_types['private']:
        pass
    elif view_type == user_view_types['public']:
        pass
    
    return render_to_response('./socialnet/user/activity.html', data)

def userNewProject(request, user_to_be_viewed, view_type, viewer):
    form = NewProjectForm(request.POST or None)
    
    data = { 'user_name': user_to_be_viewed.username,
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'new_project_form': form,
             'view': 'New Project' }
    
    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)

    
    return render(request, './socialnet/user/new_project.html', data)

def userProjects(user_to_be_viewed, view_type, viewer):
    projects = list( Project.objects.filter(owner__id=user_to_be_viewed.id) )
    
    print projects
    
    data = { 'user_name': user_to_be_viewed.username,
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'projects': projects,
             'view': 'Projects' }
    
    if view_type == user_view_types['private']:
        pass
    elif view_type == user_view_types['public']:
        pass
    
    return render_to_response('./socialnet/user/projects.html', data)

def userFriends(user_to_be_viewed, view_type, viewer):
    friends = list( User.objects.filter(additional_info__friend__id=user_to_be_viewed.id) )
    
    data = { 'user_name': user_to_be_viewed.username,
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'friends': friends,
             'view': 'Friends' }
    
    if view_type == user_view_types['private']:
        pass
    elif view_type == user_view_types['public']:
        pass
    
    return render_to_response('./socialnet/user/friends.html', data)

def userContributors(user_to_be_viewed, view_type, viewer):
    data = { 'user_name': user_to_be_viewed.username,
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'view': 'Contributors' }
    
    return render_to_response('./socialnet/user/contributors.html', data)

def userNewData(request, user_to_be_viewed, view_type, viewer):
    form = NewUserDataForm(request.POST or None)
    
    data = { 'user_name': user_to_be_viewed.username,
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'new_user_data_form': form,
             'view': 'New Data' }
    
    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)

    
    return render(request, './socialnet/user/new_data.html', data)

def userData(user_to_be_viewed, view_type, viewer):
    collected_data = list( Data.objects.filter(owner__id=user_to_be_viewed.id) )
    
    data = { 'user_name': user_to_be_viewed.username,
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'data': collected_data,
             'view': 'Data' }
    
    if view_type == user_view_types['private']:
        pass
    elif view_type == user_view_types['public']:
        pass
    
    return render_to_response('./socialnet/user/data.html', data)

def userNewAnalysis(request, user_to_be_viewed, view_type, viewer):
    form = NewUserAnalysisForm(request.POST or None)
    
    data = { 'user_name': user_to_be_viewed.username,
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'new_user_analysis_form': form,
             'view': 'New Analysis' }
    
    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)

    
    return render(request, './socialnet/user/new_analysis.html', data)

def userAnalysis(user_to_be_viewed, view_type, viewer):
    analysis_sets = []
    projects = list( Project.objects.filter(owner__id=user_to_be_viewed.id) )
    
    for project in projects:
        analysis_set = list( Analysis.objects.filter(project__id=project.id) )
        for a in analysis_set:
            analysis_sets.append( (project, a) )
    
    print analysis_sets
    
    data = { 'user_name': user_to_be_viewed.username,
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'analysis_sets': analysis_sets,
             'view': 'Analysis' }
    
    if view_type == user_view_types['private']:
        pass
    elif view_type == user_view_types['public']:
        pass
    
    return render_to_response('./socialnet/user/analysis.html', data)

def userSettings(user_to_be_viewed, view_type, viewer):
    data = { 'user_name': user_to_be_viewed.username,
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'view': 'Settings' }
    
    return render_to_response('./socialnet/user/settings.html', data)


class NewProjectForm(forms.Form):
    name = forms.CharField(max_length=200)
    public = forms.BooleanField()
    description = forms.CharField(max_length=400)
    
    contributor = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    observer = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    current_revision = forms.ModelChoiceField(queryset=Revision.objects.all())
    
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

class NewUserDataForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=400)
    file_data = forms.FileField()
    
    revision = forms.ModelChoiceField(queryset=Revision.objects.all())
    collected_location = forms.ModelChoiceField(queryset=Location.objects.all())
    host = forms.ModelChoiceField(queryset=Host.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(NewUserDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-user-data-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_data'
        self.helper.help_text_as_placeholder = True
        
        self.helper.add_input(Submit('submit', 'Submit'))

class NewUserAnalysisForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=400)
    
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    contributor = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    data = forms.ModelMultipleChoiceField(queryset=Data.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(NewUserAnalysisForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-user-analysis-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_analysis'
        self.helper.help_text_as_placeholder = True
        
        self.helper.add_input(Submit('submit', 'Submit'))
