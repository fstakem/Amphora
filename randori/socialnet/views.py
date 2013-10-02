from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User
from models import UserProfile, Project
from collections import Set

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
			return userNewProject(user_to_be_viewed, view_type, viewer)

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

def userNewProject(user_to_be_viewed, view_type, viewer):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'viewer_name': viewer.username,
			 'view_type': view_type,
			 'view': 'New Project' }

	return render_to_response('./socialnet/user/new_project.html', data)

def userProjects(user_to_be_viewed, view_type, viewer):
	projects = list( Project.objects.filter(owner__username=user_to_be_viewed.username) )

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
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'viewer_name': viewer.username,
			 'view_type': view_type,
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
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'viewer_name': viewer.username,
			 'view_type': view_type,
			 'view': 'Data' }
	
	if view_type == user_view_types['private']:
		pass
	elif view_type == user_view_types['public']:
		pass

	return render_to_response('./socialnet/user/data.html', data)

def userAnalysis(user_to_be_viewed, view_type, viewer):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'viewer_name': viewer.username,
			 'view_type': view_type,
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



	
# Attachment
def attachment(request, user_name, project_name, attachment_name):
	user = request.user
	user_page = list( User.objects.filter(username=user_name) )
	project_to_be_viewed = list( Project.objects.filter(name=project_name, owner__username=user_name) )
	attachment_page = list( Attachment.objects.filter(name=attachment_name, project__name=project_name) )

	if user_page and project_to_be_viewed and attachment_page:
		user_page = user_page[0]
		project_to_be_viewed = project_to_be_viewed[0]
		attachment_page = attachment_page[0]
		data = { 'user_name': user_page.username, 
				 'first_name': user_page.first_name,
				 'last_name': user_page.last_name,
				 'project_name':  project_to_be_viewed.name,
				 'attachment_name': attachment_page.name }

		if isUsersPageAndLoggedIn(user, user_page):
			data['private'] = True
		else:
			data['private'] = False

		return render_to_response('./socialnet/attachment.html', data)

	return HttpResponse(status=404)


# Misc
def isUsersPageAndLoggedIn(viewer, user_to_be_viewed):
	if viewer.is_authenticated() and viewer.username == user_to_be_viewed.username:
		return True
	else:
		return False













