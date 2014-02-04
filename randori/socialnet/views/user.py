# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: user.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 1.7.14
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
import re

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django import forms
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Div, Field, Reset

# App imports
from ..models import UserProfile, Project, Analysis, Data, Location, Host
from helper import is_users_page_and_logged_in

# Main
reserved_words = [ 'activities', 'projects', 'new_project', 'people', 'settings' ]

user_view_types = {'public': 'public', 'private': 'private'}

people_subviews = set([ 
                        'following',
                        'followers',
                        'contributors',
                      ])
settings_subviews = set([ 
                          'personal',
                          'account'
                      ])
subviews = set.union(people_subviews, settings_subviews)
                  
def filter_username(user_name):
    return user_name.lower()

def get_parameters(request, user_name):
    subview = ''
    view_type = user_view_types['public']
    
    try:
        view_param = request.GET['view']
        if view_param in subviews:
            subview = view_param
    except KeyError:
        pass
    
    viewer = request.user
    user_to_be_viewed = list( User.objects.filter(username=user_name) )
 
    if user_to_be_viewed:
        user_to_be_viewed = user_to_be_viewed[0]
        
        if is_users_page_and_logged_in(viewer, user_to_be_viewed):
            view_type = user_view_types['private']
        else:
            view_type = user_view_types['public']

        return [subview, view_type, viewer, user_to_be_viewed]

    else:
        return []

def user(request, user_name):
    user_name = filter_username(user_name)
    subview, view_type, viewer, user_to_be_viewed = get_parameters(request, user_name)
    location = '/' + user_to_be_viewed.username + '/activities'
    return HttpResponseRedirect(location)

def activities(request, user_name):
    user_name = filter_username(user_name)
    subview, view_type, viewer, user_to_be_viewed = get_parameters(request, user_name)

    activities = []
    projects = list( Project.objects.filter(owner__id=user_to_be_viewed.id).order_by('-date_created') )
    data = list( Data.objects.filter(owner__id=user_to_be_viewed.id).order_by('-date_uploaded') )
    analysis = list( Analysis.objects.filter(creator__id=user_to_be_viewed.id).order_by('-date_created') )

    if view_type == user_view_types['public']:
        tmp_data = []
        for d in data:
            data_project = list( Project.objects.filter(id=d.project.id) )[0]
            if data_project.public:
                tmp_data.append(d)

        data = tmp_data

        tmp_analysis = []
        for a in analysis:
            analysis_project = list( Project.objects.filter(id=a.project.id) )[0]
            if analysis_project.public:
                tmp_analysis.append(a)

        analysis = tmp_analysis

    activity_data = get_activity_data(projects, data, analysis)

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

def projects(request, user_name):
    user_name = filter_username(user_name)
    subview, view_type, viewer, user_to_be_viewed = get_parameters(request, user_name)

    projects = set(Project.objects.filter(owner__id=user_to_be_viewed.id))
    contrib_projects = list(Project.objects.filter(contributor__id=user_to_be_viewed.id))
    projects.update(contrib_projects)

    projects = list(projects)
    projects.sort(key=lambda x: x.last_activity, reverse=True)
    project_data = get_project_data(projects, user_to_be_viewed)

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

def new_project(request, user_name):
    user_name = filter_username(user_name)
    subview, view_type, viewer, user_to_be_viewed = get_parameters(request, user_name)

    form = NewProjectForm(request.POST or None)
    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'New Project',
                    'new_project_form': form,
                }

    if request.POST:
        cancel = request.POST.get('cancel', '')
        submit = request.POST.get('submit', '')

        if submit == 'Create' and form.is_valid() and user_view_types['private'] == 'private':
            name = form.cleaned_data.get('name', '')
            public = form.cleaned_data.get('public', '')
            description = form.cleaned_data.get('description', '')

            project = Project(owner=viewer, name=name, public=public, description=description)
            project.save()

            location = '/' + user_to_be_viewed.username + '/projects'
            return HttpResponseRedirect(location)

        elif cancel == 'Cancel':
            location = '/' + user_to_be_viewed.username + '/projects'
            return HttpResponseRedirect(location)

    return render(request, './socialnet/user/new_project.html', page_data)

def delete_project(request, user_name):
    user_name = filter_username(user_name)
    subview, view_type, viewer, user_to_be_viewed = get_parameters(request, user_name)

    project_name = request.GET['name']
    projects = Project.objects.filter(name=project_name)
   
    if len(projects) > 0:
        project = projects[0]
        project.delete()

    location = '/' + user_to_be_viewed.username + '/projects'
    
    return HttpResponseRedirect(location)

def leave_project(request, user_name):
    user_name = filter_username(user_name)
    subview, view_type, viewer, user_to_be_viewed = get_parameters(request, user_name)

    project_name = request.GET['name']
    projects = Project.objects.filter(name=project_name)

    if len(projects) > 0:
        project = projects[0]
        project.contributor.remove(user_to_be_viewed.id)

    location = '/' + user_to_be_viewed.username + '/projects'

    return HttpResponseRedirect(location)

def people(request, user_name):
    user_name = filter_username(user_name)
    subview, view_type, viewer, user_to_be_viewed = get_parameters(request, user_name)
    people = []
    
    action = request.GET.get('action', '')
    item = request.GET.get('item', '')

    if view_type == user_view_types['private']:
        location = '/' + user_to_be_viewed.username + '/people?view=' + subview

        if action == 'delete':
            follower = list( User.objects.filter(username=item) )[0]
            user_to_be_viewed.additional_info.followed.remove(follower)
            return HttpResponseRedirect(location)

        elif action == 'follow':
            user = list( User.objects.filter(username=item) )[0]
            user_to_be_viewed.additional_info.followed.add(user)
            return HttpResponseRedirect(location)

    following = User.objects.filter(follower__id=user_to_be_viewed.id)

    if subview == 'followers':
        people = User.objects.filter(additional_info__followed__id=user_to_be_viewed.id)
    elif subview == 'contributors':
        people = get_contributors(user_to_be_viewed)
    elif subview == 'following':
        people = following
    else:
        location = '/' + user_to_be_viewed.username + '/people?view=following'
        return HttpResponseRedirect(location)

    people_left, people_right = separate_into_columns(people, following, 2)
        
    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'People',
                    'subview': subview,
                    'people_left': people_left,
                    'people_right': people_right
                }

    return render_to_response('./socialnet/user/people.html', page_data)

def settings(request, user_name):
    user_name = filter_username(user_name)
    subview, view_type, viewer, user_to_be_viewed = get_parameters(request, user_name)

    if subview == 'account':
        return account_settings(request, user_name)
    elif subview == 'personal':
        return personal_settings(request, user_name)
    else:
        subview = 'personal'
        return personal_settings(request, user_name)

def personal_settings(request, user_name):
    user_name = filter_username(user_name)
    subview, view_type, viewer, user_to_be_viewed = get_parameters(request, user_name)

    user_profile = UserProfile.objects.filter(user__id=user_to_be_viewed.id)[0]

    form = None
    subview = 'personal'
    first_name = user_to_be_viewed.first_name
    last_name = user_to_be_viewed.last_name
    email = user_to_be_viewed.email
    website = user_profile.personal_website
    github_page = user_profile.github_page
    title = user_profile.title

    form = ChangeSettingsForm(request.POST or None, first_name=first_name, last_name=last_name, 
                              email=email, website=website,  github_page=github_page, title=title)
    
    if request.POST:
        cancel = request.POST.get('cancel', '')
        update = request.POST.get('update', '')
        
        if update == 'Update' and user_view_types['private'] == 'private':
           
            if form.is_valid():
                user_to_be_viewed.first_name = form.cleaned_data.get('first_name', '')
                user_to_be_viewed.last_name = form.cleaned_data.get('last_name', '')
                user_to_be_viewed.email = form.cleaned_data.get('email', '')
                user_to_be_viewed.save()

                user_profile.personal_website = form.cleaned_data.get('personal_website', '')
                user_profile.github_page = form.cleaned_data.get('github_page', '')
                user_profile.title = form.cleaned_data.get('title', '')
                user_profile.save()

                location = '/' + user_to_be_viewed.username + '/settings?view=personal'
                return HttpResponseRedirect(location)
                
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            website = request.POST.get('personal_website', '')
            github_page = request.POST.get('github_page', '')
            title = request.POST.get('title', '')

            form = ChangeSettingsForm(request.POST or None, first_name=first_name, last_name=last_name, 
                              email=email, website=website,  github_page=github_page, title=title)

        elif cancel == 'Cancel':
            location = '/' + user_to_be_viewed.username + '/settings?view=personal'
            return HttpResponseRedirect(location)

    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'Settings',
                    'subview': subview,
                    'change_settings_form': form,
                }
    
    return render_to_response('./socialnet/user/personal_settings.html', page_data, context_instance=RequestContext(request))

def account_settings(request, user_name):
    user_name = filter_username(user_name)
    subview, view_type, viewer, user_to_be_viewed = get_parameters(request, user_name)

    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'Settings',
                    'subview': subview,
                }

    return render_to_response('./socialnet/user/account_settings.html', page_data)

def get_contributors(user_to_be_viewed):
    contributors = set()
    projects = Project.objects.filter(owner__id=user_to_be_viewed.id)

    for project in projects:
        temp_contributors = User.objects.filter(contributed_project__id=project.id)

        for temp in temp_contributors:
            if temp not in contributors and temp != user_to_be_viewed:
                contributors.add(temp)

    contributors = list(contributors)

    return contributors

def separate_into_columns(people, following, num_of_cols):
    columns = []

    for i in range(num_of_cols):
        columns.append([])

    if len(people) > 0:
        people = list(people)
        people.sort(key=lambda x: x.username)
        people_data = get_personal_data(people, following)

        for i, data in enumerate(people_data):
            r = i % num_of_cols
            columns[r].append(data)

    return columns

def get_personal_data(people, following):
    personal_data = []
    following = set(following)

    for person in people:
        if person in following:
            personal_data.append( [person.username, person.additional_info.title, person.additional_info.profile_photo.url, True] )
        else:
            personal_data.append( [person.username, person.additional_info.title, person.additional_info.profile_photo.url, False] )

    return personal_data

def get_project_data(projects, user_to_be_viewed):
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

def get_activity_data(projects, data, analysis):
    activity_data = []

    for project in projects:
        created = project.date_created.strftime("%B %d at %I:%M %p")
        activity_data.append(['project', project.name, created])
            
    for d in data:
        created = d.date_uploaded.strftime("%B %d at %I:%M %p")
        activity_data.append(['data', d.name, created])

    for a in analysis:
        created = a.date_created.strftime("%B %d at %I:%M %p")
        activity_data.append(['analysis', a.name, created])

    activity_data.sort(key=lambda x: x[2], reverse=True)

    return activity_data

class NewProjectForm(forms.Form):
    name = forms.CharField(max_length=200)
    public = forms.BooleanField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 5}))
    
    def __init__(self, *args, **kwargs):
        super(NewProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-project-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-3'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_project'
        self.helper.help_text_as_placeholder = True
        
        self.helper.layout = Layout(
            Field('name', title="Name", value='', placeholder='New project name'),
            Field('public', title="Last name"),
            Field('description', title="Description", placeholder='This is a software development project.'),
            Div( 
                Submit('cancel', 'Cancel', css_class="btn btn-primary"),
                Submit('submit', 'Create', css_class="btn btn-success"),
                css_class='col-lg-offset-2 col-lg-6' 
                ),
        )

    def clean_name(self):
        data = self.cleaned_data['name']
        filtered_data = filter_username(data)

        projects = Project.objects.filter(name=filtered_data)
        if len(projects) > 0:
            raise forms.ValidationError('Project name is taken.')

        tokens = filtered_data.strip().split()
        filtered_data = '_'.join(tokens)

        if not re.match(r'^[a-zA-Z0-9_-]+$', filtered_data):
            raise forms.ValidationError('AlphaNumeric characters only.')

        return filtered_data

class ChangeSettingsForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    personal_website = forms.URLField(required=False, max_length=200)
    github_page = forms.URLField(required=False, max_length=200)
    profile_photo = forms.ImageField(required=False)
    cover_photo = forms.ImageField(required=False)
    title = forms.CharField(required=False, max_length=200)
    # Dont know how to initialize field
    #bio = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 5}))
    
    def __init__(self, *args, **kwargs):
        self.first_name = kwargs.pop('first_name')
        self.last_name = kwargs.pop('last_name')
        self.email = kwargs.pop('email')
        self.website = kwargs.pop('website')
        self.github_page = kwargs.pop('github_page')
        self.title = kwargs.pop('title')

        super(ChangeSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-change-settings-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.form_method = 'post'
        self.helper.form_action = 'settings'
        self.helper.help_text_as_placeholder = True

        #ChangeSettingsForm.__dict__['base_fields']['bio'].initial = user_profile.bio
        
        self.helper.layout = Layout(
            Field('first_name', title="First name", value=self.first_name),
            Field('last_name', title="Last name", value=self.last_name),
            Field('email', title="Email", value=self.email),
            Field('personal_website', title="Personal website", value=self.website),
            Field('github_page', title="Github page", value=self.github_page),
            Field('title', title="Title", value=self.title),
            Field('profile_photo', title="Profile photo"),
            Field('cover_photo', title="Cover photo"),
            #Field('bio', title="Bio", initial=user_profile.bio),
            Div( 
                Submit('cancel', 'Cancel', css_class="button-default"),
                Submit('update', 'Update', css_class="btn-success"),
                css_class='col-lg-offset-2 col-lg-6' 
                ),
        )












