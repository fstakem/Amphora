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
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django import forms
from django.core.context_processors import csrf

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Div, Field, Reset

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
    activities_per_page = 10
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

    activity_data = getActivityData(projects, data, analysis)

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
    
    action = request.GET.get('action', '')
    item = request.GET.get('item', '')

    if view_type == user_view_types['private']:
        if action == 'delete':
            follower = list( User.objects.filter(username=item) )[0]
            user_to_be_viewed.additional_info.followed.remove(follower)
            return HttpResponseRedirect('/' + user_to_be_viewed.username + '/?view=people_' + sub_view)

        elif action == 'follow':
            user = list( User.objects.filter(username=item) )[0]
            user_to_be_viewed.additional_info.followed.add(user)
            return HttpResponseRedirect('/' + user_to_be_viewed.username + '/?view=people_' + sub_view)

    following = User.objects.filter(follower__id=user_to_be_viewed.id)
    
    if sub_view == 'followers':
        people = User.objects.filter(additional_info__followed__id=user_to_be_viewed.id)
    elif sub_view == 'contributors':
        people = getContributors(user_to_be_viewed)
    else:
        people = following

    people_left, people_right = separateIntoColumns(people, following, 2)
        
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
    if sub_view == 'account':
        return accountSettings(request, sub_view, user_to_be_viewed, view_type, viewer)
    else:
        return personalSettings(request, sub_view, user_to_be_viewed, view_type, viewer)

def personalSettings(request, sub_view, user_to_be_viewed, view_type, viewer):
    user_profile = UserProfile.objects.filter(user__id=user_to_be_viewed.id)[0]
    print '-----HERE-------'
    #print request.POST.get('first_name', '')
    #print request.POST.get('last_name', '')
    form = ChangeSettingsForm(user_to_be_viewed, user_profile, request.POST or None)
    #print request.POST.get('first_name', '')
    #print request.POST.get('last_name', '')
    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'Settings',
                    'sub_view': sub_view,
                    'change_settings_form': form,
                }

    if request.POST and form.is_valid():
        print 'POST form bro'
    
    return render_to_response('./socialnet/user/personal_settings.html', page_data)

def accountSettings(request, sub_view, user_to_be_viewed, view_type, viewer):
    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'Settings',
                    'sub_view': sub_view,
                }

    return render_to_response('./socialnet/user/account_settings.html', page_data)

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

def separateIntoColumns(people, following, num_of_cols):
    columns = []

    for i in range(num_of_cols):
        columns.append([])

    if len(people) > 0:
        people = list(people)
        people.sort(key=lambda x: x.username)
        people_data = getPersonalData(people, following)

        for i, data in enumerate(people_data):
            r = i % num_of_cols
            columns[r].append(data)

    return columns

def getPersonalData(people, following):
    personal_data = []
    following = set(following)

    for person in people:
        if person in following:
            personal_data.append( [person.username, person.additional_info.title, person.additional_info.profile_photo.url, True] )
        else:
            personal_data.append( [person.username, person.additional_info.title, person.additional_info.profile_photo.url, False] )

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

def getActivityData(projects, data, analysis):
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

class ChangeSettingsForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    personal_website = forms.URLField(max_length=200)
    github_page = forms.URLField(max_length=200)
    profile_photo = forms.ImageField(required=False)
    cover_photo = forms.ImageField(required=False)
    title = forms.CharField(max_length=200)
    # Dont know how to initialize field
    #bio = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 5}))
    
    def __init__(self, user, user_profile, *args, **kwargs):
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
            Field('first_name', title="First name", value=user.first_name),
            Field('last_name', title="Last name", value=user.last_name),
            Field('email', title="Email", value=user.email),
            Field('personal_website', title="Personal website", value=user_profile.personal_website),
            Field('github_page', title="Github page", value=user_profile.github_page),
            Field('title', title="Title", value=user_profile.title),
            Field('profile_photo', title="Profile photo"),
            Field('cover_photo', title="Cover photo"),
            #Field('bio', title="Bio", initial=user_profile.bio),
            Div( 
                Reset('cancel', 'Cancel', css_class="button-default"),
                Submit('update', 'Update', css_class="btn-success"),
                css_class='col-lg-offset-2 col-lg-6' 
                ),
        )












