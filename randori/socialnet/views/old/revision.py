# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: revision.py
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
revision_view_types = {'public': 'public', 'contributor': 'contributor', 'owner': 'owner'}
revision_views = set([ 'info',
                       'activity',
                       'data',
                       'new_data',
                       'settings' ])

revision_views = set([ 'info',
                       'activity',
                       'data',
                       'new_data',
                       'settings' ])

def revision(request, user_name, project_name, revision_name):
    view = 'activity'
    view_type = revision_view_types['public']
    
    try:
        view_param = request.GET['view']
        if view_param in revision_views:
            view = view_param
    except KeyError:
        pass
    
    viewer = request.user
    project_owner = list( User.objects.filter(username=user_name) )
    project_contributors = list( User.objects.filter(contributed_project__name=project_name) )
    project_to_be_viewed = list( Project.objects.filter(name=project_name, owner__username=user_name) )
    project_revison = list( Revision.objects.filter(project__name=project_name) )
    
    if project_to_be_viewed and project_owner and project_revison:
        project_owner = project_owner[0]
        project_to_be_viewed = project_to_be_viewed[0]
        project_revison = project_revison[0]
        
        if viewer.is_authenticated():
            if viewer.username == project_owner.username:
                view_type = revision_view_types['owner']
            else:
                for c in project_contributors:
                    if c.username == viewer.username:
                        view_type = revision_view_types['contributor']
                        break
        
        if view == 'info':
            return revisionInfo(project_owner, project_to_be_viewed, project_revison, view_type, viewer)
        
        elif view == 'activity':
            return revisionActivity(project_owner, project_to_be_viewed, project_revison, view_type, viewer)
        
        elif view == 'data':
            return revisionData(project_owner, project_to_be_viewed, project_revison, view_type, viewer)
        
        elif view == 'new_data' and (view_type == revision_view_types['owner'] or view_type == revision_view_types['contributor']):
            return revisionNewData(request, project_owner, project_to_be_viewed, project_revison, view_type, viewer)
        
        else:
            return HttpResponse(status=404)
    
    return HttpResponse(status=404)

def revisionActivity(project_owner, project_to_be_viewed, project_revison, view_type, viewer):
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'revision_name': project_revison.name(),
             'view': 'Activity' }
    
    if view_type == revision_view_types['owner'] or view_type == revision_view_types['contributor']:
        pass
    elif view_type == revision_view_types['public']:
        pass
    
    return render_to_response('./socialnet/revision/activity.html', data)

def revisionInfo(project_owner, project_to_be_viewed, project_revison, view_type, viewer):
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'revision_name': project_revison.name(),
             'view': 'Info' }
    
    if view_type == revision_view_types['owner'] or view_type == revision_view_types['contributor']:
        pass
    elif view_type == revision_view_types['public']:
        pass
    
    return render_to_response('./socialnet/revision/info.html', data)

def revisionData(project_owner, project_to_be_viewed, project_revison, view_type, viewer):
    rev_data = list( Data.objects.filter(revision__id=project_revison.id) )
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'revision_name': project_revison.name(),
             'rev_data': rev_data,
             'view': 'Data' }
    
    if view_type == revision_view_types['owner'] or view_type == revision_view_types['contributor']:
        pass
    elif view_type == revision_view_types['public']:
        pass
    
    return render_to_response('./socialnet/revision/data.html', data)

def revisionNewData(request, project_owner, project_to_be_viewed, project_revison, view_type, viewer):
    form = NewRevisionDataForm(request.POST or None)
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'revision_name': project_revison.name(),
             'new_revision_data_form': form,
             'view': 'New Data' }
    
    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)

    
    return render(request, './socialnet/revision/new_data.html', data)

class NewRevisionDataForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=400)
    file_data = forms.FileField()
    
    collected_location = forms.ModelChoiceField(queryset=Location.objects.all())
    host = forms.ModelChoiceField(queryset=Host.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(NewRevisionDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-user-data-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_data'
        self.helper.help_text_as_placeholder = True
        
        self.helper.add_input(Submit('submit', 'Submit'))