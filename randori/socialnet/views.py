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

project_views = set([ 'activity', 
					  'people', 
					  'data',
					  'analysis', 
					  'settings' ])

# User
def user(request, user_name):
	view = 'activity'
	view_types = {'public': 0, 'private': 1}
	view_type = view_types['public']

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
			view_type = view_types['private']
		else:
			view_type = view_types['public']

		if view == 'activity' and view_type == view_types['private']:
			return userPrivateActivity(user_to_be_viewed)
		elif view == 'activity' and view_type == view_types['public']:
			return userPublicActivity(user_to_be_viewed, viewer)
		elif view == 'new_project' and view_type == view_types['private']:
			return userPrivateNewProject(user_to_be_viewed)
		elif view == 'projects' and view_type == view_types['private']:
			return userPrivateProjects(user_to_be_viewed)
		elif view == 'projects' and view_type == view_types['public']:
			return userPublicProjects(user_to_be_viewed, viewer)
		elif view == 'friends' and view_type == view_types['private']:
			return userPrivateFriends(user_to_be_viewed)
		elif view == 'friends' and view_type == view_types['public']:
			return userPublicFriends(user_to_be_viewed, viewer)
		elif view == 'contributors' and view_type == view_types['private']:
			return userPrivateContributors(user_to_be_viewed)
		elif view == 'data' and view_type == view_types['private']:
			return userPrivateData(user_to_be_viewed)
		elif view == 'data' and view_type == view_types['public']:
			return userPublicData(user_to_be_viewed, viewer)
		elif view == 'analysis' and view_type == view_types['private']:
			return userPrivateAnalysis(user_to_be_viewed)
		elif view == 'analysis' and view_type == view_types['public']:
			return userPublicAnalysis(user_to_be_viewed, viewer)
		elif view == 'settings' and view_type == view_types['private']:
			return userPrivateSettings(user_to_be_viewed)
		else:
			return HttpResponse(status=404)

	return HttpResponse(status=404)

def userPublicActivity(user_to_be_viewed, viewer):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'viewer_name': viewer.username,
			 'view': 'Activity' }
	return render_to_response('./socialnet/user_public_activity.html', data)

def userPrivateActivity(user_to_be_viewed):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'view': 'Activity' }
	return render_to_response('./socialnet/user_private_activity.html', data)

def userPrivateNewProject(user_to_be_viewed):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'view': 'New Project' }
	return render_to_response('./socialnet/user_private_new_project.html', data)

def userPublicProjects(user_to_be_viewed, viewer):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'viewer_name': viewer.username,
			 'view': 'Projects' }
	return render_to_response('./socialnet/user_public_projects.html', data)

def userPrivateProjects(user_to_be_viewed):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'view': 'Projects' }
	return render_to_response('./socialnet/user_private_projects.html', data)

def userPublicFriends(user_to_be_viewed, viewer):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'viewer_name': viewer.username,
			 'view': 'Friends' }
	return render_to_response('./socialnet/user_public_friends.html', data)

def userPrivateFriends(user_to_be_viewed):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'view': 'Friends' }
	return render_to_response('./socialnet/user_private_friends.html', data)

def userPrivateContributors(user_to_be_viewed):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'view': 'Contributors' }
	return render_to_response('./socialnet/user_private_contributors.html', data)

def userPublicData(user_to_be_viewed, viewer):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'viewer_name': viewer.username,
			 'view': 'Data' }
	return render_to_response('./socialnet/user_public_data.html', data)

def userPrivateData(user_to_be_viewed):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'view': 'Data' }
	return render_to_response('./socialnet/user_private_data.html', data)

def userPublicAnalysis(user_to_be_viewed, viewer):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'viewer_name': viewer.username,
			 'view': 'Analysis' }
	return render_to_response('./socialnet/user_public_analysis.html', data)

def userPrivateAnalysis(user_to_be_viewed):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'view': 'Analysis' }
	return render_to_response('./socialnet/user_private_analysis.html', data)

def userPrivateSettings(user_to_be_viewed):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'view': 'Settings' }
	return render_to_response('./socialnet/user_private_settings.html', data)


# Project
def project(request, user_name, project_name):
	view = 'activity'
	view_types = {'public': 0, 'contributor': 1, 'owner': 2}
	view_type = view_types['public']

	try:
		view_param = request.GET['view']
		if view_param in project_views:
			view = view_param
	except KeyError:
		pass

	viewer = request.user
	user_page = list( User.objects.filter(username=user_name) )
	project_page = list( Project.objects.filter(name=project_name, owner__username=user_name) )

	if user_page and project_page:
		user_page = user_page[0]
		project_page = project_page[0]
		
		if isUsersPageAndLoggedIn(viewer, user_page):
			private = True
		else:
			private = False

		if project_page.owner.username == viewer.username:
			owner = True
		else:
			owner = False

		print owner

		if view == 'activity' and private == True:
			return projectPrivateActivity(user_page, project_page, owner)
		elif view == 'activity' and private == False:
			return projectPublicActivity(user_page, project_page, viewer)
		elif view == 'people' and private == True:
			return projectPrivatePeople(user_page, project_page, owner)
		elif view == 'people' and private == False:
			return projectPublicPeople(user_page, project_page, viewer)
		elif view == 'data' and private == True:
			return projectPrivateData(user_page, project_page, owner)
		elif view == 'data' and private == False:
			return projectPublicData(user_page, project_page, viewer)
		elif view == 'analysis' and private == True:
			return projectPrivateAnalysis(user_page, project_page, owner)
		elif view == 'analysis' and private == False:
			return projectPublicAnalysis(user_page, project_page, viewer)
		elif view == 'settings' and private == True:
			return projectPrivateSettings(user_page, project_page, owner)
		else:
			return HttpResponse(status=404)

		return render_to_response('./socialnet/project.html', data)
	
	return HttpResponse(status=404)

def projectPublicActivity(user_page, project_page, viewer):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'viewer_name': viewer.username,
			 'project_name':  project_page.name,
			 'view': 'Activity' }
	return render_to_response('./socialnet/project_public_activity.html', data)

def projectPrivateActivity(user_page, project_page, owner):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'project_name':  project_page.name,
			 'view': 'Activity' }
	return render_to_response('./socialnet/project_private_activity.html', data)

def projectPublicPeople(user_page, project_page, viewer):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'viewer_name': viewer.username,
			 'project_name':  project_page.name,
			 'view': 'People' }
	return render_to_response('./socialnet/project_public_people.html', data)

def projectPrivatePeople(user_page, project_page, owner):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'project_name':  project_page.name,
			 'view': 'People' }
	return render_to_response('./socialnet/project_private_people.html', data)

def projectPublicData(user_page, project_page, viewer):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'viewer_name': viewer.username,
			 'project_name':  project_page.name,
			 'view': 'Data' }
	return render_to_response('./socialnet/project_public_data.html', data)

def projectPrivateData(user_page, project_page, owner):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'project_name':  project_page.name,
			 'view': 'Data' }
	return render_to_response('./socialnet/project_private_data.html', data)

def projectPublicAnalysis(user_page, project_page, viewer):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'viewer_name': viewer.username,
			 'project_name':  project_page.name,
			 'view': 'Analysis' }
	return render_to_response('./socialnet/project_public_analysis.html', data)

def projectPrivateAnalysis(user_page, project_page, owner):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'project_name':  project_page.name,
			 'view': 'Analysis' }
	return render_to_response('./socialnet/project_private_analysis.html', data)

def projectPrivateSettings(user_page, project_page, owner):
	data = { 'user_name': user_page.username, 
			 'first_name': user_page.first_name,
			 'last_name': user_page.last_name,
			 'project_name':  project_page.name,
			 'view': 'Settings' }
	return render_to_response('./socialnet/project_private_settings.html', data)



	
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













