from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
                        url(r'^/$', views.user, name='views.user'),
                        url(r'^/activities$', views.activities, name='views.activities'),
                        url(r'^/projects$', views.projects, name='views.projects'),
                        url(r'^/new_project$', views.new_project, name='views.new_project'),
                        url(r'^/delete_project$', views.delete_project, name='views.delete_project'),
                        url(r'^/leave_project$', views.leave_project, name='views.leave_project'),
                        url(r'^/people$', views.people, name='views.people'),
                        url(r'^/settings$', views.settings, name='views.settings'),
                        url(r'^/(?P<project_name>[\w\-]+)/$', views.project, name='views.project'),
                        url(r'^/(?P<project_name>[\w\-]+)/analysis/(?P<analysis_name>[\w\-]+)/$', views.analysis, name='views.analysis'),
                      )


