from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User
from models import UserProfile, Project
from collections import Set

user_views = set([ 'activity', 
				   'new_project',
				   'projects', 
				   'friends',
				   'contributors', 
				   'data',
				   'analysis', 
				   'settings' ])

project_views = set([ 'Activity', 'People', 'Content', 'Settings' ])

# User
def user(request, user_name):
	view = 'activity'
	private = False

	try:
		view_param = request.GET['view']
		if view_param in user_views:
			view = view_param
	except KeyError:
		pass

	viewer = request.user
	print viewer
	user_page = list( User.objects.filter(username=user_name) )

	if user_page:
		user_page = user_page[0]

		if isUsersPageAndLoggedIn(viewer, user_page):
			private = True
		else:
			private = False

		if view == 'activity' and private == True:
			return userPrivateActivity(request, user_name, user_page)
		elif view == 'activity' and private == False:
			return userPublicActivity(request, user_name, user_page, viewer)
		elif view == 'new_project' and private == True:
			return userPrivateNewProject(request, user_name, user_page)
		elif view == 'projects' and private == True:
			return userPrivateProjects(request, user_name, user_page)
		elif view == 'projects' and private == False:
			return userPublicProjects(request, user_name, user_page, viewer)
		elif view == 'friends' and private == True:
			return userPrivateFriends(request, user_name, user_page)
		elif view == 'friends' and private == False:
			return userPublicFriends(request, user_name, user_page, viewer)
		elif view == 'contributors' and private == True:
			return userPrivateContributors(request, user_name, user_page)
		elif view == 'data' and private == True:
			return userPrivateData(request, user_name, user_page)
		elif view == 'data' and private == False:
			return userPublicData(request, user_name, user_page, viewer)
		elif view == 'analysis' and private == True:
			return userPrivateAnalysis(request, user_name, user_page)
		elif view == 'analysis' and private == False:
			return userPublicAnalysis(request, user_name, user_page, viewer)
		elif view == 'settings' and private == True:
			return userPrivateSettings(request, user_name, user_page)
		else:
			return HttpResponse(status=404)

	return HttpResponse(status=404)

def userPublicActivity(request, user_name, user_page, viewer):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'viewer_name': viewer.username,
			 'view': 'Activity' }
	return render_to_response('./socialnet/user_public_activity.html', data)

def userPrivateActivity(request, user_name, user_page):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'view': 'Activity' }
	return render_to_response('./socialnet/user_private_activity.html', data)

def userPrivateNewProject(request, user_name, user_page):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'view': 'New Project' }
	return render_to_response('./socialnet/user_private_new_project.html', data)

def userPublicProjects(request, user_name, user_page, viewer):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'viewer_name': viewer.username,
			 'view': 'Projects' }
	return render_to_response('./socialnet/user_public_projects.html', data)

def userPrivateProjects(request, user_name, user_page):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'view': 'Projects' }
	return render_to_response('./socialnet/user_private_projects.html', data)

def userPublicFriends(request, user_name, user_page, viewer):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'viewer_name': viewer.username,
			 'view': 'Friends' }
	return render_to_response('./socialnet/user_public_friends.html', data)

def userPrivateFriends(request, user_name, user_page):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'view': 'Friends' }
	return render_to_response('./socialnet/user_private_friends.html', data)

def userPrivateContributors(request, user_name, user_page):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'view': 'Contributors' }
	return render_to_response('./socialnet/user_private_contributors.html', data)

def userPublicData(request, user_name, user_page, viewer):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'viewer_name': viewer.username,
			 'view': 'Data' }
	return render_to_response('./socialnet/user_public_data.html', data)

def userPrivateData(request, user_name, user_page):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'view': 'Data' }
	return render_to_response('./socialnet/user_private_data.html', data)

def userPublicAnalysis(request, user_name, user_page, viewer):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'viewer_name': viewer.username,
			 'view': 'Analysis' }
	return render_to_response('./socialnet/user_public_analysis.html', data)

def userPrivateAnalysis(request, user_name, user_page):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'view': 'Analysis' }
	return render_to_response('./socialnet/user_private_analysis.html', data)

def userPrivateSettings(request, user_name, user_page):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'view': 'Settings' }
	return render_to_response('./socialnet/user_private_settings.html', data)


# Project
def project(request, user_name, project_name):
	view = 'Activity'
	try:
		view_param = request.GET['view']
		if view_param in project_views:
			view = view_param
	except KeyError:
		pass

	user = request.user
	user_page = list( User.objects.filter(username=user_name) )
	project_page = list( Project.objects.filter(name=project_name, owner__username=user_name) )

	if user_page and project_page:
		user_page = user_page[0]
		project_page = project_page[0]
		data = { 'user_name': user_page.username, 
				 'first_name': user_page.first_name,
				 'last_name': user_page.last_name,
				 'project_name':  project_page.name,
				 'view': view  }

		if isUsersPageAndLoggedIn(user, user_page):
			data['private'] = True
		else:
			data['private'] = False

		return render_to_response('./socialnet/project.html', data)
	
	return HttpResponse(status=404)

	
# Attachment
def attachment(request, user_name, project_name, attachment_name):
	user = request.user
	user_page = list( User.objects.filter(username=user_name) )
	project_page = list( Project.objects.filter(name=project_name, owner__username=user_name) )
	attachment_page = list( Attachment.objects.filter(name=attachment_name, project__name=project_name) )

	if user_page and project_page and attachment_page:
		user_page = user_page[0]
		project_page = project_page[0]
		attachment_page = attachment_page[0]
		data = { 'user_name': user_page.username, 
				 'first_name': user_page.first_name,
				 'last_name': user_page.last_name,
				 'project_name':  project_page.name,
				 'attachment_name': attachment_page.name }

		if isUsersPageAndLoggedIn(user, user_page):
			data['private'] = True
		else:
			data['private'] = False

		return render_to_response('./socialnet/attachment.html', data)

	return HttpResponse(status=404)


# Misc
def isUsersPageAndLoggedIn(viewer, user_page):
	if viewer.is_authenticated() and viewer.username == user_page.username:
		return True
	else:
		return False











