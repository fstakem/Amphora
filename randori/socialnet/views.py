from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from models import UserProfile, Project, Analysis, Data, Revision, Location, Host, SoftwareStack, Version
from collections import Set
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

user_view_types = {'public': 'public', 'private': 'private'}
user_views = set([ 'info',
				   'activity', 
				   'new_project',
				   'projects', 
				   'friends', 
				   'contributors',
				   'new_data', 
				   'data',
				   'analysis',
				   'new_analysis', 
				   'settings' ])

project_view_types = {'public': 'public', 'contributor': 'contributor', 'owner': 'owner'}
project_views = set([ 'info',
                      'activity', 
					  'people', 
					  'revisions',
                      'new_revision',
					  'analysis', 
                      'new_analysis',
					  'settings' ])

revision_view_types = {'public': 'public', 'contributor': 'contributor', 'owner': 'owner'}
revision_views = set([ 'info',
                       'activity', 
                       'data',
                       'new_data',
                       'settings' ])

data_view_types = {'public': 'public', 'contributor': 'contributor', 'owner': 'owner'}
data_views = set([ 'info',
                       'activity'])

analysis_view_types = {'public': 'public', 'contributor': 'contributor', 'owner': 'owner'}
analysis_views = set([ 'info',
                       'activity'])

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

		if view == 'info':
			return userInfo(user_to_be_viewed, view_type, viewer)

		elif view == 'activity':
			return userActivity(user_to_be_viewed, view_type, viewer)
		
		elif view == 'new_project' and view_type == user_view_types['private']:
			return userNewProject(request, user_to_be_viewed, view_type, viewer)

		elif view == 'projects':
			return userProjects(user_to_be_viewed, view_type, viewer)

		elif view == 'friends':
			return userFriends(user_to_be_viewed, view_type, viewer)

		elif view == 'contributors' and view_type == user_view_types['private']:
			return userContributors(user_to_be_viewed, view_type, viewer)

		elif view == 'new_data' and view_type == user_view_types['private']:
			return userNewData(request, user_to_be_viewed, view_type, viewer)

		elif view == 'data':
			return userData(user_to_be_viewed, view_type, viewer)

		elif view == 'new_analysis' and view_type == user_view_types['private']:
			return userNewAnalysis(request, user_to_be_viewed, view_type, viewer)

		elif view == 'analysis':
			return userAnalysis(user_to_be_viewed, view_type, viewer)

		elif view == 'settings' and view_type == user_view_types['private']:
			return userSettings(user_to_be_viewed, view_type, viewer)

		else:
			return HttpResponse(status=404)

	return HttpResponse(status=404)

def userInfo(user_to_be_viewed, view_type, viewer):
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'viewer_name': viewer.username,
			 'view_type': view_type,
			 'view': 'Info' }

	if view_type == user_view_types['private']:
		pass
	elif view_type == user_view_types['public']:
		pass

	return render_to_response('./socialnet/user/info.html', data)

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

	print projects

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
	friends = list( User.objects.filter(additional_info__friend__id=user_to_be_viewed.id) )

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

def userNewData(request, user_to_be_viewed, view_type, viewer):
    form = NewUserDataForm(request.POST or None)

    data = { 'user_name': user_to_be_viewed.username, 
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'new_user_data_form': form,
             'view': 'New Data' }

    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)


    return render(request, './socialnet/user/new_data.html', data)

def userData(user_to_be_viewed, view_type, viewer):
	collected_data = list( Data.objects.filter(owner__id=user_to_be_viewed.id) )
	
	data = { 'user_name': user_to_be_viewed.username, 
			 'first_name': user_to_be_viewed.first_name,
			 'last_name': user_to_be_viewed.last_name,
			 'viewer_name': viewer.username,
			 'view_type': view_type,
			 'data': collected_data,
			 'view': 'Data' }
	
	if view_type == user_view_types['private']:
		pass
	elif view_type == user_view_types['public']:
		pass

	return render_to_response('./socialnet/user/data.html', data)

def userNewAnalysis(request, user_to_be_viewed, view_type, viewer):
    form = NewUserAnalysisForm(request.POST or None)

    data = { 'user_name': user_to_be_viewed.username, 
             'first_name': user_to_be_viewed.first_name,
             'last_name': user_to_be_viewed.last_name,
             'viewer_name': viewer.username,
             'view_type': view_type,
             'new_user_analysis_form': form,
             'view': 'New Analysis' }

    if request.POST and form.is_valid():
        print 'POST form bro'
        #user = form.login(request)
        #if user:
        #    auth.login(request, user)
        #    return HttpResponseRedirect("/" + user.username)


    return render(request, './socialnet/user/new_analysis.html', data)


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

        if view == 'info':
            return projectInfo(project_owner, project_to_be_viewed, view_type, viewer)

        elif view == 'activity':
            return projectActivity(project_owner, project_to_be_viewed, view_type, viewer)

        elif view == 'people':
            return projectPeople(project_owner, project_to_be_viewed, view_type, viewer)

        elif view == 'revisions':
            return projectRevisions(project_owner, project_to_be_viewed, view_type, viewer)

        elif view == 'new_revision' and (view_type == project_view_types['owner'] or view_type == project_view_types['contributor']):
            return projectNewRevision(request, project_owner, project_to_be_viewed, view_type, viewer)

        elif view == 'analysis':
            return projectAnalysis(project_owner, project_to_be_viewed, view_type, viewer)

        elif view == 'new_analysis' and (view_type == project_view_types['owner'] or view_type == project_view_types['contributor']):
            return projectNewAnalysis(request, project_owner, project_to_be_viewed, view_type, viewer)

        elif view == 'settings' and view_type == project_view_types['owner']:
            return projectSettings(project_owner, project_to_be_viewed, view_type, viewer)

        else:
            return HttpResponse(status=404)

	return HttpResponse(status=404)

def projectInfo(project_owner, project_to_be_viewed, view_type, viewer):
    data = { 'user_name': project_owner.username, 
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'view': 'Info' }

    if view_type == project_view_types['owner'] or view_type == project_view_types['contributor']:
        pass
    elif view_type == project_view_types['public']:
        pass

    return render_to_response('./socialnet/project/info.html', data)

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

def projectSettings(project_owner, project_to_be_viewed, view_type, viewer):
	data = { 'user_name': project_owner.username, 
			 'first_name': project_owner.first_name,
			 'last_name': project_owner.last_name,
			 'project_name':  project_to_be_viewed.name,
			 'view_type': view_type,
			 'viewer_name': viewer.username,
			 'view': 'Settings' }

	return render_to_response('./socialnet/project/settings.html', data)

# Revision
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


# Data
def data(request, user_name, project_name, revision_name, data_name):
    view = 'activity'
    view_type = data_view_types['public']

    try:
        view_param = request.GET['view']
        if view_param in data_views:
            view = view_param
    except KeyError:
        pass

    viewer = request.user
    project_owner = list( User.objects.filter(username=user_name) )
    project_contributors = list( User.objects.filter(contributed_project__name=project_name) )
    project_to_be_viewed = list( Project.objects.filter(name=project_name, owner__username=user_name) )
    project_revison = list( Revision.objects.filter(project__name=project_name) )
    revision_data = list( Data.objects.filter(name=data_name) )

    if project_to_be_viewed and project_owner and project_revison and revision_data:
        project_owner = project_owner[0]
        project_to_be_viewed = project_to_be_viewed[0]
        project_revison = project_revison[0]
        revision_data = revision_data[0]

        if viewer.is_authenticated():
            if viewer.username == project_owner.username:
                view_type = data_view_types['owner']
            else:
                for c in project_contributors:
                    if c.username == viewer.username:
                        view_type = data_view_types['contributor']
                        break

        if view == 'info':
            return dataInfo(project_owner, project_to_be_viewed, project_revison, revision_data, view_type, viewer)

        elif view == 'activity':
            return dataActivity(project_owner, project_to_be_viewed, project_revison, revision_data, view_type, viewer)

        else:
            return HttpResponse(status=404)

    return HttpResponse(status=404)

def dataInfo(project_owner, project_to_be_viewed, project_revison, revision_data, view_type, viewer):
    data = { 'user_name': project_owner.username, 
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'revision_name': project_revison.name(),
             'data_name': revision_data.name,
             'view': 'Info' }

    if view_type == revision_view_types['owner'] or view_type == revision_view_types['contributor']:
        pass
    elif view_type == revision_view_types['public']:
        pass

    return render_to_response('./socialnet/data/info.html', data)

def dataActivity(project_owner, project_to_be_viewed, project_revison, revision_data, view_type, viewer):
    data = { 'user_name': project_owner.username, 
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'revision_name': project_revison.name(),
             'data_name': revision_data.name,
             'view': 'Activity' }

    if view_type == revision_view_types['owner'] or view_type == revision_view_types['contributor']:
        pass
    elif view_type == revision_view_types['public']:
        pass

    return render_to_response('./socialnet/data/activity.html', data)

# Analysis
def analysis(request, user_name, project_name, analysis_name):
    view = 'activity'
    view_type = analysis_view_types['public']

    try:
        view_param = request.GET['view']
        if view_param in analysis_views:
            view = view_param
    except KeyError:
        pass

    viewer = request.user
    project_owner = list( User.objects.filter(username=user_name) )
    project_contributors = list( User.objects.filter(contributed_project__name=project_name) )
    project_to_be_viewed = list( Project.objects.filter(name=project_name, owner__username=user_name) )
    project_analysis = list( Analysis.objects.filter(project__name=project_name) )

    if project_to_be_viewed and project_owner and project_analysis:
        project_owner = project_owner[0]
        project_to_be_viewed = project_to_be_viewed[0]
        project_analysis = project_analysis[0]

        if viewer.is_authenticated():
            if viewer.username == project_owner.username:
                view_type = analysis_view_types['owner']
            else:
                for c in project_contributors:
                    if c.username == viewer.username:
                        view_type = analysis_view_types['contributor']
                        break

        if view == 'info':
            return analysisInfo(project_owner, project_to_be_viewed, project_analysis, view_type, viewer)

        elif view == 'activity':
            return analysisActivity(project_owner, project_to_be_viewed, project_analysis, view_type, viewer)

        else:
            return HttpResponse(status=404)

    return HttpResponse(status=404)

def analysisActivity(project_owner, project_to_be_viewed, project_analysis, view_type, viewer):
    data = { 'user_name': project_owner.username, 
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'analysis_name': project_analysis.name,
             'view': 'Activity' }

    if view_type == revision_view_types['owner'] or view_type == revision_view_types['contributor']:
        pass
    elif view_type == revision_view_types['public']:
        pass

    return render_to_response('./socialnet/analysis/activity.html', data)

def analysisInfo(project_owner, project_to_be_viewed, project_analysis, view_type, viewer):
    data = { 'user_name': project_owner.username, 
             'first_name': project_owner.first_name,
             'last_name': project_owner.last_name,
             'view_type': view_type,
             'viewer_name': viewer.username,
             'project_name':  project_to_be_viewed.name,
             'analysis_name': project_analysis.name,
             'view': 'Info' }

    if view_type == revision_view_types['owner'] or view_type == revision_view_types['contributor']:
        pass
    elif view_type == revision_view_types['public']:
        pass

    return render_to_response('./socialnet/analysis/info.html', data)


	
# Forms
class NewProjectForm(forms.Form):
    name = forms.CharField(max_length=200)
    public = forms.BooleanField()
    description = forms.CharField(max_length=400)

    contributor = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    observer = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    current_revision = forms.ModelChoiceField(queryset=Revision.objects.all())

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

class NewUserDataForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=400)
    file_data = forms.FileField()

    revision = forms.ModelChoiceField(queryset=Revision.objects.all())
    collected_location = forms.ModelChoiceField(queryset=Location.objects.all())
    host = forms.ModelChoiceField(queryset=Host.objects.all())

    def __init__(self, *args, **kwargs):
        super(NewUserDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-user-data-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_data'
        self.helper.help_text_as_placeholder = True

        self.helper.add_input(Submit('submit', 'Submit'))

class NewUserAnalysisForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=400)

    project = forms.ModelChoiceField(queryset=Project.objects.all())
    contributor = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    data = forms.ModelMultipleChoiceField(queryset=Data.objects.all())

    def __init__(self, *args, **kwargs):
        super(NewUserAnalysisForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-user-analysis-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_analysis'
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

# Misc
def isUsersPageAndLoggedIn(viewer, user_to_be_viewed):
	if viewer.is_authenticated() and viewer.username == user_to_be_viewed.username:
		return True
	else:
		return False













