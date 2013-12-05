# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: project.py
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
project_view_types = {'public': 'public', 'contributor': 'contributor', 'owner': 'owner'}
project_views = set([ 'info',
                      'activity',
                      'people',
                      'revisions',
                      'data',
                      'analysis',
                      'settings',
                      'new_person',
                      'new_revision',
                      'new_data',
                      'new_analysis' ])

def project(request, user_name, project_name):
    view = 'activity'
    view_type = project_view_types['public']
    
    try:
        view_param = request.GET['view']
        if view_param in project_views:
            view = view_param
    except KeyError:
        pass
    
    viewer = request.user
    project_owner = list( User.objects.filter(username=user_name) )
    project_contributors = list( User.objects.filter(contributed_project__name=project_name) )
    project_to_be_viewed = list( Project.objects.filter(name=project_name, owner__username=user_name) )
    
    if project_to_be_viewed and project_owner:
        project_owner = project_owner[0]
        project_to_be_viewed = project_to_be_viewed[0]
        
        if viewer.is_authenticated():
            if viewer.username == project_owner.username:
                view_type = project_view_types['owner']
            else:
                for c in project_contributors:
                    if c.username == viewer.username:
                        view_type = project_view_types['contributor']
                        break
        
        # Public views
        if view == 'info':
            return projectInfo(request, project_owner, project_to_be_viewed, view_type, viewer)
        
        elif view == 'activity':
            return projectActivity(project_owner, project_to_be_viewed, view_type, viewer)
        
        elif view == 'people':
            return projectPeople(project_owner, project_to_be_viewed, view_type, viewer)
        
        elif view == 'revisions':
            return projectRevisions(project_owner, project_to_be_viewed, view_type, viewer)
        
        elif view == 'data':
            return projectData(project_owner, project_to_be_viewed, view_type, viewer)
        
        elif view == 'analysis':
            return projectAnalysis(project_owner, project_to_be_viewed, view_type, viewer)
        
        # Private views
        elif view == 'settings' and view_type == project_view_types['owner']:
            return projectSettings(project_owner, project_to_be_viewed, view_type, viewer)
        
        elif view == 'new_person' and (view_type == project_view_types['owner'] or view_type == project_view_types['contributor']):
            return projectNewPerson(request, project_owner, project_to_be_viewed, view_type, viewer)
        
        elif view == 'new_revision' and (view_type == project_view_types['owner'] or view_type == project_view_types['contributor']):
            return projectNewRevision(request, project_owner, project_to_be_viewed, view_type, viewer)
        
        elif view == 'new_data' and (view_type == project_view_types['owner'] or view_type == project_view_types['contributor']):
            return projectNewData(request, project_owner, project_to_be_viewed, view_type, viewer)
        
        elif view == 'new_analysis' and (view_type == project_view_types['owner'] or view_type == project_view_types['contributor']):
            return projectNewAnalysis(request, project_owner, project_to_be_viewed, view_type, viewer)
        
        # No view
        else:
            return HttpResponse(status=404)
    
    return HttpResponse(status=404)

# Public views
def projectActivity(project_owner, project_to_be_viewed, view_type, viewer):
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'view': 'Activity' }
    
    if view_type == project_view_types['owner'] or view_type == project_view_types['contributor']:
        pass
    elif view_type == project_view_types['public']:
        pass
    
    return render_to_response('./socialnet/project/activity.html', data)

def projectInfo(request, project_owner, project_to_be_viewed, view_type, viewer):
    if request.POST:
        project = Project.objects.get(pk=request.POST['pk'])
        
        if request.POST['name'] == 'name':
            print 'Whoa buddy! We need some more logic before you go bout doin that.'
        elif request.POST['name'] == 'public':
            value = True
            if request.POST['value'] == '0':
                value = False

            setattr(project, request.POST['name'], value)
        else:
            setattr(project, request.POST['name'], request.POST['value'])
            
        project.save()

        revisions = list( Revision.objects.filter(project__id=project_to_be_viewed.id).prefetch_related('version') )

        contributors = list( User.objects.filter(contributed_project__id=project_to_be_viewed.id) )
        observers = list( User.objects.filter(watched_project__id=project_to_be_viewed.id) )
        #url = request.META['PATH_INFO'][1:] + '?' + request.META['QUERY_STRING']
        url = '?' + request.META['QUERY_STRING']
        ui_data = { 'project_name': {'a': 1, 'b': 2, 'c': 3} }

        
        data = { 'user_name': project_owner.username,
                 'first_name': project_owner.first_name,
                 'last_name': project_owner.last_name,
                 'view_type': view_type,
                 'viewer_name': viewer.username,
                 'project_name':  project_to_be_viewed.name,
                 'public': project_to_be_viewed.public,
                 'current_revision': project_to_be_viewed.current_revision,
                 'revisions': revisions,
                 'description': project_to_be_viewed.description,
                 'owner': project_to_be_viewed.owner,
                 'contributors': contributors,
                 'observers': observers,
                 'url': url,
                 'ui_data': ui_data,
                 'project_id': project_to_be_viewed.id, 
                 'view': 'Info' }
        
        return render_to_response('./socialnet/project/info.html', data)
    else:
        revisions = list( Revision.objects.filter(project__id=project_to_be_viewed.id).prefetch_related('version') )
        for revision in revisions:
            print revision.id 
            print revision.version

        contributors = list( User.objects.filter(contributed_project__id=project_to_be_viewed.id) )
        observers = list( User.objects.filter(watched_project__id=project_to_be_viewed.id) )
        #url = request.META['PATH_INFO'][1:] + '?' + request.META['QUERY_STRING']
        url = '?' + request.META['QUERY_STRING']
        ui_data = { 'project_name': {'a': 1, 'b': 2, 'c': 3} }

        
        data = { 'user_name': project_owner.username,
                 'first_name': project_owner.first_name,
                 'last_name': project_owner.last_name,
                 'view_type': view_type,
                 'viewer_name': viewer.username,
                 'project_name':  project_to_be_viewed.name,
                 'public': project_to_be_viewed.public,
                 'current_revision': project_to_be_viewed.current_revision,
                 'revisions': revisions,
                 'description': project_to_be_viewed.description,
                 'owner': project_to_be_viewed.owner,
                 'contributors': contributors,
                 'observers': observers,
                 'url': url,
                 'ui_data': ui_data,
                 'project_id': project_to_be_viewed.id, 
                 'view': 'Info' }
        
        if view_type == project_view_types['owner'] or view_type == project_view_types['contributor']:
            pass
        elif view_type == project_view_types['public']:
            pass
        
        return render_to_response('./socialnet/project/info.html', data)

def projectPeople(project_owner, project_to_be_viewed, view_type, viewer):
    owner = project_to_be_viewed.owner
    contributors = list( User.objects.filter(contributed_project__id=project_to_be_viewed.id) )
    observers = list( User.objects.filter(watched_project__id=project_to_be_viewed.id) )
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name': project_to_be_viewed.name,
             'owner': owner,
             'contributors': contributors,
             'observers': observers,
             'view': 'People' }
    
    if view_type == project_view_types['owner'] or view_type == project_view_types['contributor']:
        pass
    elif view_type == project_view_types['public']:
        pass
    
    return render_to_response('./socialnet/project/people.html', data)

def projectRevisions(project_owner, project_to_be_viewed, view_type, viewer):
    revisions = list( Revision.objects.filter(project__id=project_to_be_viewed.id) )
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'revisions': revisions,
             'view': 'Revisions' }
    
    if view_type == project_view_types['owner'] or view_type == project_view_types['contributor']:
        pass
    elif view_type == project_view_types['public']:
        pass
    
    return render_to_response('./socialnet/project/revisions.html', data)

def projectData(project_owner, project_to_be_viewed, view_type, viewer):
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'view': 'Data' }
    
    if view_type == project_view_types['owner'] or view_type == project_view_types['contributor']:
        pass
    elif view_type == project_view_types['public']:
        pass
    
    return render_to_response('./socialnet/project/data.html', data)

def projectAnalysis(project_owner, project_to_be_viewed, view_type, viewer):
    analysis = list( Analysis.objects.filter(project__id=project_to_be_viewed.id) )
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'analysis': analysis,
             'view': 'Analysis' }
    
    if view_type == project_view_types['owner'] or view_type == project_view_types['contributor']:
        pass
    elif view_type == project_view_types['public']:
        pass
    
    return render_to_response('./socialnet/project/analysis.html', data)

# Private views
def projectSettings(project_owner, project_to_be_viewed, view_type, viewer):
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'project_name':  project_to_be_viewed.name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'view': 'Settings' }
    
    return render_to_response('./socialnet/project/settings.html', data)

def projectNewPerson(request, project_owner, project_to_be_viewed, view_type, viewer):
    form = NewProjectPersonForm(request.POST or None)
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'new_project_person_form': form,
             'view': 'New Person' }
    
    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)

    
    return render(request, './socialnet/project/new_person.html', data)

def projectNewRevision(request, project_owner, project_to_be_viewed, view_type, viewer):
    form = NewProjectRevisionForm(request.POST or None)
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'new_project_revision_form': form,
             'view': 'New Revision' }
    
    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)

    
    return render(request, './socialnet/project/new_revision.html', data)

def projectNewData(request, project_owner, project_to_be_viewed, view_type, viewer):
    form = NewProjectDataForm(request.POST or None)
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'new_project_data_form': form,
             'view': 'New Data' }
    
    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)

    
    return render(request, './socialnet/project/new_data.html', data)

def projectNewAnalysis(request, project_owner, project_to_be_viewed, view_type, viewer):
    form = NewProjectAnalysisForm(request.POST or None)
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'new_project_analysis_form': form,
             'view': 'New Analysis' }
    
    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)

    
    return render(request, './socialnet/project/new_analysis.html', data)

class NewProjectPersonForm(forms.Form):
    version = forms.ModelChoiceField(queryset=Version.objects.all())
    software_stack = forms.ModelMultipleChoiceField(queryset=SoftwareStack.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(NewProjectPersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-project-person-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_person'
        self.helper.help_text_as_placeholder = True
        
        self.helper.add_input(Submit('submit', 'Submit'))

class NewProjectRevisionForm(forms.Form):
    version = forms.ModelChoiceField(queryset=Version.objects.all())
    software_stack = forms.ModelMultipleChoiceField(queryset=SoftwareStack.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(NewProjectRevisionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-project-revision-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_revision'
        self.helper.help_text_as_placeholder = True
        
        self.helper.add_input(Submit('submit', 'Submit'))

class NewProjectDataForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=400)
    file_data = forms.FileField()
    
    collected_location = forms.ModelChoiceField(queryset=Location.objects.all())
    host = forms.ModelChoiceField(queryset=Host.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(NewProjectDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-project-data-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_data'
        self.helper.help_text_as_placeholder = True
        
        self.helper.add_input(Submit('submit', 'Submit'))

class NewProjectAnalysisForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=400)
    
    contributor = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    data = forms.ModelMultipleChoiceField(queryset=Data.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(NewProjectAnalysisForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-project-analysis-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_analysis'
        self.helper.help_text_as_placeholder = True
        
        self.helper.add_input(Submit('submit', 'Submit'))