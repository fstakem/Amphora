# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: data.py
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

# Main
data_view_types = {'public': 'public', 'contributor': 'contributor', 'owner': 'owner'}
data_views = set([ 'info',
                       'activity'])

def data(request, user_name, project_name, revision_name, data_name):
    view = 'activity'
    view_type = data_view_types['public']
    
    try:
        view_param = request.GET['view']
        if view_param in data_views:
            view = view_param
    except KeyError:
        pass
    
    viewer = request.user
    project_owner = list( User.objects.filter(username=user_name) )
    project_contributors = list( User.objects.filter(contributed_project__name=project_name) )
    project_to_be_viewed = list( Project.objects.filter(name=project_name, owner__username=user_name) )
    project_revison = list( Revision.objects.filter(project__name=project_name) )
    revision_data = list( Data.objects.filter(name=data_name) )
    
    if project_to_be_viewed and project_owner and project_revison and revision_data:
        project_owner = project_owner[0]
        project_to_be_viewed = project_to_be_viewed[0]
        project_revison = project_revison[0]
        revision_data = revision_data[0]
        
        if viewer.is_authenticated():
            if viewer.username == project_owner.username:
                view_type = data_view_types['owner']
            else:
                for c in project_contributors:
                    if c.username == viewer.username:
                        view_type = data_view_types['contributor']
                        break
        
        if view == 'info':
            return dataInfo(project_owner, project_to_be_viewed, project_revison, revision_data, view_type, viewer)
        
        elif view == 'activity':
            return dataActivity(project_owner, project_to_be_viewed, project_revison, revision_data, view_type, viewer)
        
        else:
            return HttpResponse(status=404)
    
    return HttpResponse(status=404)

def dataInfo(project_owner, project_to_be_viewed, project_revison, revision_data, view_type, viewer):
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'revision_name': project_revison.name(),
             'data_name': revision_data.name,
             'view': 'Info' }
    
    if view_type == revision_view_types['owner'] or view_type == revision_view_types['contributor']:
        pass
    elif view_type == revision_view_types['public']:
        pass
    
    return render_to_response('./socialnet/data/info.html', data)

def dataActivity(project_owner, project_to_be_viewed, project_revison, revision_data, view_type, viewer):
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'revision_name': project_revison.name(),
             'data_name': revision_data.name,
             'view': 'Activity' }
    
    if view_type == revision_view_types['owner'] or view_type == revision_view_types['contributor']:
        pass
    elif view_type == revision_view_types['public']:
        pass
    
    return render_to_response('./socialnet/data/activity.html', data)
