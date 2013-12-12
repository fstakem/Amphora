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
view_types = {'public': 'public', 'contributor': 'contributor', 'owner': 'owner'}
views = set([ 'info',
              'activity',
              'people',
              'add_person',
              'person_requests',
              'graph_hosts',
              'tree_hosts',
              'data',
              'analysis',
              'settings',
              'new_revision',
              'new_data',
              'new_analysis' ])

def project(request, user_name, project_name):
    view = 'activity'
    view_type = view_types['public']
    
    try:
        view_param = request.GET['view']
        if view_param in views:
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
                view_type = view_types['owner']
            else:
                for c in project_contributors:
                    if c.username == viewer.username:
                        view_type = view_types['contributor']
                        break
        
        # Public views
        if view == 'info':
            return infoView(request, project_owner, project_to_be_viewed, view, view_type, viewer)
        
        elif view == 'activity':
            return activityView(project_owner, project_to_be_viewed, view, view_type, viewer)
        
        elif view == 'people':
            return peopleView(project_owner, project_to_be_viewed, view, view_type, viewer)
        
        elif view == 'graph_hosts':
            return graphHostsView(project_owner, project_to_be_viewed, view, view_type, viewer)

        elif view == 'tree_hosts':
            return treeHostsView(project_owner, project_to_be_viewed, view, view_type, viewer)
        
        elif view == 'data':
            return dataView(project_owner, project_to_be_viewed, view, view_type, viewer)
        
        elif view == 'analysis':
            return analysisView(project_owner, project_to_be_viewed, view, view_type, viewer)
        
        # Private views
        elif view == 'settings' and view_type == view_types['owner']:
            return settingsView(project_owner, project_to_be_viewed, view, view_type, viewer)
        
        elif view == 'add_person' and (view_type == view_types['owner'] or view_type == view_types['contributor']):
            return addPersonView(request, project_owner, project_to_be_viewed, view, view_type, viewer)

        elif view == 'person_requests' and view_type == view_types['owner']:
            return personRequestView(request, project_owner, project_to_be_viewed, view, view_type, viewer)
        
        elif view == 'new_data' and (view_type == view_types['owner'] or view_type == view_types['contributor']):
            return newDataView(request, project_owner, project_to_be_viewed, view, view_type, viewer)
        
        elif view == 'new_analysis' and (view_type == view_types['owner'] or view_type == view_types['contributor']):
            return newAnalysisView(request, project_owner, project_to_be_viewed, view, view_type, viewer)
        
        # No view
        else:
            return HttpResponse(status=404)
    
    return HttpResponse(status=404)

# Public views
def activityView(project_owner, project_to_be_viewed, view, view_type, viewer):
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'view': 'activity' }
    
    if view_type == view_types['owner'] or view_type == view_types['contributor']:
        pass
    elif view_type == view_types['public']:
        pass
    
    return render_to_response('./socialnet/project/activity.html', data)

def infoView(request, project_owner, project_to_be_viewed, view, view_type, viewer):
    if request.POST:
        project = Project.objects.get(pk=request.POST['pk'])
        
        if request.POST['name'] == 'name':
            print 'Whoa buddy! We need some more logic before you go bout doin that.'
        elif request.POST['name'] == 'public':
            value = True
            if request.POST['value'] == '0':
                value = False

            setattr(project, request.POST['name'], value)
        elif request.POST['name'] == 'owner':
            print 'Whoa buddy! We need some more logic before you go bout doin that.'
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
                 'view': 'info' }
        
        return render_to_response('./socialnet/project/info.html', data)
    else:
        revisions = list( Revision.objects.filter(project__id=project_to_be_viewed.id).prefetch_related('version') )
        revision_data = []
        for revision in revisions:
            revision_data.append( [revision.id, str(revision.version) ] )
        revision_data = simplejson.dumps(revision_data)
        current_revision = [project_to_be_viewed.current_revision.id, str(project_to_be_viewed.current_revision.version)]
        current_revision = simplejson.dumps(current_revision)


        contributors = list( User.objects.filter(contributed_project__id=project_to_be_viewed.id) )
        contributor_data = []
        for contributor in contributors:
            print contributor
            contributor_data.append( [contributor.id, str(contributor.username) ] )
        contributor_data = simplejson.dumps(contributor_data)

        owner = project_to_be_viewed.owner
        owner_data = simplejson.dumps( [owner.id, str(owner.username) ] )

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
                 'current_revision': current_revision,
                 'revisions': revision_data,
                 'description': project_to_be_viewed.description,
                 'owner': owner_data,
                 'contributors': contributor_data,
                 'contrib_alt': contributors,
                 'observers': observers,
                 'url': url,
                 'ui_data': ui_data,
                 'project_id': project_to_be_viewed.id, 
                 'view': 'info' }
        
        if view_type == view_types['owner'] or view_type == view_types['contributor']:
            pass
        elif view_type == view_types['public']:
            pass
        
        return render_to_response('./socialnet/project/info.html', data)

def peopleView(project_owner, project_to_be_viewed, view, view_type, viewer):
    owner = project_to_be_viewed.owner
    contributors = list( User.objects.filter(contributed_project__id=project_to_be_viewed.id) )

    users = set(contributors) 
    users.add(owner)
    users = list(users)
    users.sort(key=lambda x: x.username)

    user_data_left = []
    user_data_right = []
    for i, user in enumerate(users):
        if i % 2 == 0:
            user_data_left.append( getPersonalInformation(user, owner) )
        else:
            user_data_right.append( getPersonalInformation(user, owner) )
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name': project_to_be_viewed.name,
             'owner': owner,
             'users_left': user_data_left,
             'users_right': user_data_right,
             'view': 'people' }
    
    if view_type == view_types['owner'] or view_type == view_types['contributor']:
        return render_to_response('./socialnet/project/private_people.html', data)
    elif view_type == view_types['public']:
        return render_to_response('./socialnet/project/public_people.html', data)

def getPersonalInformation(user, owner):
    role = 'contributor'
    if owner != None and owner.id == user.id:
        role = 'owner'

    data = [user.username, 'Software Engineer', role, user.additional_info.profile_photo.url]

    return data

def graphHostsView(project_owner, project_to_be_viewed, view, view_type, viewer):
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'view': 'graph_hosts' }
    
    if view_type == view_types['owner'] or view_type == view_types['contributor']:
        pass
    elif view_type == view_types['public']:
        pass
    
    return render_to_response('./socialnet/project/hosts.html', data)

def treeHostsView(project_owner, project_to_be_viewed, view, view_type, viewer):
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'view': 'tree_hosts' }
    
    if view_type == view_types['owner'] or view_type == view_types['contributor']:
        pass
    elif view_type == view_types['public']:
        pass
    
    return render_to_response('./socialnet/project/hosts.html', data)

def dataView(project_owner, project_to_be_viewed, view, view_type, viewer):
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'view': 'data' }
    
    if view_type == view_types['owner'] or view_type == view_types['contributor']:
        pass
    elif view_type == view_types['public']:
        pass
    
    return render_to_response('./socialnet/project/data.html', data)

def analysisView(project_owner, project_to_be_viewed, view, view_type, viewer):
    analysis = list( Analysis.objects.filter(project__id=project_to_be_viewed.id) )
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'analysis': analysis,
             'view': 'analysis' }
    
    if view_type == view_types['owner'] or view_type == view_types['contributor']:
        pass
    elif view_type == view_types['public']:
        pass
    
    return render_to_response('./socialnet/project/analysis.html', data)

# Private views
def settingsView(project_owner, project_to_be_viewed, view, view_type, viewer):
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'project_name':  project_to_be_viewed.name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'view': 'settings' }
    
    return render_to_response('./socialnet/project/settings.html', data)

def addPersonView(request, project_owner, project_to_be_viewed, view, view_type, viewer):
    owner = project_to_be_viewed.owner
    # change this to other contributors -> waiting to be accepted
    contributors = list( User.objects.filter(contributed_project__id=project_to_be_viewed.id) )

    users = set(contributors) 
    users = list(users)
    users.sort(key=lambda x: x.username)

    user_data_left = []
    user_data_right = []

    for i, user in enumerate(users):
        if i % 2 == 0:
            user_data_left.append( getPersonalInformation(user, None) )
        else:
            user_data_right.append( getPersonalInformation(user, None) )
    
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name': project_to_be_viewed.name,
             'owner': owner,
             'users_left': user_data_left,
             'users_right': user_data_right,
             'view': 'add_person' }
    
    return render_to_response('./socialnet/project/private_people.html', data)

def personRequestView(request, project_owner, project_to_be_viewed, view, view_type, viewer):
    owner = project_to_be_viewed.owner
    # change this to other contributors -> waiting to be accepted
    contributors = list( User.objects.filter(contributed_project__id=project_to_be_viewed.id) )

    users = set(contributors) 
    users = list(users)
    users.sort(key=lambda x: x.username)

    user_data_left = []
    user_data_right = []
    for i, user in enumerate(users):
        if i % 2 == 0:
            user_data_left.append( getPersonalInformation(user, None) )
        else:
            user_data_right.append( getPersonalInformation(user, None) )
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name': project_to_be_viewed.name,
             'owner': owner,
             'users_left': user_data_left,
             'users_right': user_data_right,
             'view': 'person_requests' }
    
    return render_to_response('./socialnet/project/private_people.html', data)
        
def newDataView(request, project_owner, project_to_be_viewed, view, view_type, viewer):
    form = NewDataForm(request.POST or None)
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'new_project_data_form': form,
             'view': 'new_data' }
    
    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)

    
    return render(request, './socialnet/project/new_data.html', data)

def newAnalysisView(request, project_owner, project_to_be_viewed, view, view_type, viewer):
    form = NewAnalysisForm(request.POST or None)
    
    data = { 'user_name': project_owner.username,
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'new_project_analysis_form': form,
             'view': 'new_analysis' }
    
    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)

    
    return render(request, './socialnet/project/new_analysis.html', data)

class NewPersonForm(forms.Form):
    version = forms.ModelChoiceField(queryset=Version.objects.all())
    software_stack = forms.ModelMultipleChoiceField(queryset=SoftwareStack.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(NewPersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-project-person-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_person'
        self.helper.help_text_as_placeholder = True
        
        self.helper.add_input(Submit('submit', 'Submit'))

class NewDataForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=400)
    file_data = forms.FileField()
    
    collected_location = forms.ModelChoiceField(queryset=Location.objects.all())
    host = forms.ModelChoiceField(queryset=Host.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(NewDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-project-data-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_data'
        self.helper.help_text_as_placeholder = True
        
        self.helper.add_input(Submit('submit', 'Submit'))

class NewAnalysisForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=400)
    
    contributor = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    data = forms.ModelMultipleChoiceField(queryset=Data.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(NewAnalysisForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-project-analysis-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_analysis'
        self.helper.help_text_as_placeholder = True
        
        self.helper.add_input(Submit('submit', 'Submit'))



