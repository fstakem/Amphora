from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from models import UserProfile, Project, Analysis, Data
from collections import Set
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

user_view_types = {'public': 'public', 'private': 'private'}
user_views = set([ 'activity', 
				   'new_project',
				   'projects', 
				   'friends',
				   'contributors', 
				   'data',
				   'analysis', 
				   'settings' ])

project_view_types = {'public': 'public', 'contributor': 'contributor', 'owner': 'owner'}
project_views = set([ 'activity', 
					  'people', 
					  'data',
					  'analysis', 
					  'settings' ])

# User
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

		if view == 'activity':
			return userActivity(user_to_be_viewed, view_type, viewer)
		
		elif view == 'new_project' and view_type == user_view_types['private']:
			return userNewProject(request, user_to_be_viewed, view_type, viewer)

		elif view == 'projects':
			return userProjects(user_to_be_viewed, view_type, viewer)

		elif view == 'friends':
			return userFriends(user_to_be_viewed, view_type, viewer)

		elif view == 'contributors' and view_type == user_view_types['private']:
			return userContributors(user_to_be_viewed, view_type, viewer)

		elif view == 'data':
			return userData(user_to_be_viewed, view_type, viewer)

		elif view == 'analysis':
			return userAnalysis(user_to_be_viewed, view_type, viewer)

		elif view == 'settings' and view_type == user_view_types['private']:
			return userSettings(user_to_be_viewed, view_type, viewer)

		else:
			return HttpResponse(status=404)

	return HttpResponse(status=404)

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
	friends = list( User.objects.filter(friend__id=user_to_be_viewed.id) )

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

def userData(user_to_be_viewed, view_type, viewer):
	data_sets = []
	projects = list( Project.objects.filter(owner__id=user_to_be_viewed.id) )
	
	for project in projects:
		data_set = list( Data.objects.filter(project__id=project.id) )
		for d in data_set:
			data_sets.append( (project, d) )

	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'viewer_name': viewer.username,
			 'view_type': view_type,
			 'data_sets': data_sets,
			 'view': 'Data' }
	
	if view_type == user_view_types['private']:
		pass
	elif view_type == user_view_types['public']:
		pass

	return render_to_response('./socialnet/user/data.html', data)

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


# Project
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

		if view == 'activity':
			return projectActivity(project_owner, project_to_be_viewed, view_type, viewer)

		elif view == 'people':
			return projectPeople(project_owner, project_to_be_viewed, view_type, viewer)

		elif view == 'data':
			return projectData(project_owner, project_to_be_viewed, view_type, viewer)

		elif view == 'analysis':
			return projectAnalysis(project_owner, project_to_be_viewed, view_type, viewer)

		elif view == 'settings' and view_type == project_view_types['owner']:
			return projectSettings(project_owner, project_to_be_viewed, view_type, viewer)

		else:
			return HttpResponse(status=404)

	return HttpResponse(status=404)

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

def projectPeople(project_owner, project_to_be_viewed, view_type, viewer):
	data = { 'user_name': project_owner.username, 
			 'first_name': project_owner.first_name,
			 'last_name': project_owner.last_name,
			 'view_type': view_type,
			 'viewer_name': viewer.username,
			 'project_name':  project_to_be_viewed.name,
			 'view': 'People' }
	
	if view_type == project_view_types['owner'] or view_type == project_view_types['contributor']:
		pass
	elif view_type == project_view_types['public']:
		pass

	return render_to_response('./socialnet/project/people.html', data)

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
	data = { 'user_name': project_owner.username, 
			 'first_name': project_owner.first_name,
			 'last_name': project_owner.last_name,
			 'view_type': view_type,
			 'viewer_name': viewer.username,
			 'project_name':  project_to_be_viewed.name,
			 'view': 'Analysis' }
	
	if view_type == project_view_types['owner'] or view_type == project_view_types['contributor']:
		pass
	elif view_type == project_view_types['public']:
		pass

	return render_to_response('./socialnet/project/analysis.html', data)

def projectSettings(project_owner, project_to_be_viewed, view_type, viewer):
	data = { 'user_name': project_owner.username, 
			 'first_name': project_owner.first_name,
			 'last_name': project_owner.last_name,
			 'project_name':  project_to_be_viewed.name,
			 'view_type': view_type,
			 'viewer_name': viewer.username,
			 'view': 'Settings' }

	return render_to_response('./socialnet/project/settings.html', data)

# Data
def data(request, user_name, project_name, data_name):
	data = { 'user_name': user_name, 
			 'project_name': project_name,
			 'data_name': data_name,
			 'view': 'Data' }

	return render_to_response('./socialnet/data/tmp.html', data)

# Analysis
def analysis(request, user_name, project_name, analysis_name):
	data = { 'user_name': user_name, 
			 'project_name': project_name,
			 'analysis_name': analysis_name,
			 'view': 'Data' }

	return render_to_response('./socialnet/analysis/tmp.html', data)

	
# Forms
class NewProjectForm(forms.Form):
    name = forms.CharField(max_length=200)
    date_created = forms.DateTimeField()
    last_activity = forms.DateTimeField()
    public = forms.BooleanField()
    description = forms.CharField(max_length=400)

    owner = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    contributor = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        super(NewProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-project-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_project'
        self.helper.help_text_as_placeholder = True

        self.helper.add_input(Submit('submit', 'Submit'))


# Misc
def isUsersPageAndLoggedIn(viewer, user_to_be_viewed):
	if viewer.is_authenticated() and viewer.username == user_to_be_viewed.username:
		return True
	else:
		return False













