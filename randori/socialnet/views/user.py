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
from django.http import HttpResponse
from django.shortcuts import render_to_response

# App imports
from ..models import UserProfile, Project, Analysis, Data, Location, Host
from helper import isUsersPageAndLoggedIn

# Main
user_view_types = {'public': 'public', 'private': 'private'}
user_views = set([ 'activity',
                   'projects_all',
                   'projects_new',
                   'people_following',
                   'people_followers',
                   'people_contributors',
                   'settings_personal',
                   'settings_account'
                    ])

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

        views = view.split('_')
        view_base = views[0]
        sub_view = ''

        if len(views) > 1:
            sub_view = views[1]
        
        if view_base == 'activity':
            return activity(user_to_be_viewed, view_type, viewer)

        elif view_base == 'projects':
            return projects(sub_view, user_to_be_viewed, view_type, viewer)
        
        elif view_base == 'people':
            return people(sub_view, user_to_be_viewed, view_type, viewer)

        elif view_base == 'settings' and view_type == user_view_types['private']:
            return settings(sub_view, user_to_be_viewed, view_type, viewer)
        
        else:
            return HttpResponse(status=404)
    
    return HttpResponse(status=404)

def activity(user_to_be_viewed, view_type, viewer):
    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'Activity'
                }
    
    return render_to_response('./socialnet/user/activity.html', page_data)

def projects(sub_view, user_to_be_viewed, view_type, viewer):
    if sub_view == 'new':
        return newProject(user_to_be_viewed, view_type, viewer)
    else:
        return allProjects(user_to_be_viewed, view_type, viewer)

def allProjects(user_to_be_viewed, view_type, viewer):
    projects = list(Project.objects.filter(owner__id=user_to_be_viewed.id))
    projects.sort(key=lambda x: x.last_activity, reverse=True)
    project_data = getProjectData(projects)

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

def newProject(user_to_be_viewed, view_type, viewer):
    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'Projects'
                }

    return render_to_response('./socialnet/user/new_project.html', page_data)

def people(sub_view, user_to_be_viewed, view_type, viewer):
    people = []
    
    if sub_view == 'followers':
        people = User.objects.filter(additional_info__followed__id=user_to_be_viewed.id)
    elif sub_view == 'contributors':
        people = getContributors(user_to_be_viewed)
    else:
        people = User.objects.filter(follower__id=user_to_be_viewed.id)

    people_left, people_right = separateIntoColumns(people, 2)
        
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

def settings(sub_view, user_to_be_viewed, view_type, viewer):
    page_data = {
                    'user_name': user_to_be_viewed.username,
                    'first_name': user_to_be_viewed.first_name,
                    'last_name': user_to_be_viewed.last_name,
                    'viewer_name': viewer.username,
                    'view_type': view_type,
                    'view': 'Settings',
                    'sub_view': sub_view,
                }
    
    return render_to_response('./socialnet/user/settings.html', page_data)


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

def separateIntoColumns(people, num_of_cols):
    columns = []

    for i in range(num_of_cols):
        columns.append([])

    if len(people) > 0:
        people = list(people)
        people.sort(key=lambda x: x.username)
        people_data = getPersonalData(people)

        for i, data in enumerate(people_data):
            r = i % num_of_cols
            columns[r].append(data)

    return columns

def getPersonalData(people):
    personal_data = []

    for person in people:
        personal_data.append( [person.username, person.additional_info.title, person.additional_info.profile_photo.url] )

    return personal_data

def getProjectData(projects):
    project_data = []

    for project in projects:
        last_activity = project.last_activity.strftime("%B %d")
        print last_activity
        project_data.append([project.name, last_activity, project.description, project.website, project.public])

    return project_data









