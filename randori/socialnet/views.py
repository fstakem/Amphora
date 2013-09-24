from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User
from models import UserProfile, Project
from collections import Set

user_views = set([ 'Activity', 'Projects', 'Friends', 'Content', 'Settings' ])
project_views = set([ 'Activity', 'People', 'Content', 'Settings' ])

# User
def user(request, user_name):
	view = 'Activity'
	try:
		view_param = request.GET['view']
		if view_param in user_views:
			view = view_param
	except KeyError:
		pass

	user = request.user
	user_page = list( User.objects.filter(username=user_name) )

	if user_page:
		user_page = user_page[0]
		data = { 'user_name': user_page.username, 
				 'first_name': user_page.first_name,
				 'last_name': user_page.last_name,
				 'view': view }

		if isUsersPageAndLoggedIn(user, user_page):
			data['private'] = True
		else:
			data['private'] = False

		return render_to_response('./socialnet/user.html', data)

	return HttpResponse(status=404)

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
def isUsersPageAndLoggedIn(user, user_page):
	if user.is_authenticated() and user.username == user_page.username:
		return True
	else:
		return False











