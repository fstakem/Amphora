from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
                       url(r'^/$', views.user, name='views.user'),
                       url(r'^/(?P<project_name>[\w\-]+)/$', views.project, name='views.project'),
                       url(r'^/(?P<project_name>[\w\-]+)/(?P<revision_name>[\w\-]+)/$', views.revision, name='views.revision'),
                       url(r'^/(?P<project_name>[\w\-]+)/analysis/(?P<analysis_name>[\w\-]+)/$', views.analysis, name='views.analysis'),
                       url(r'^/(?P<project_name>[\w\-]+)/(?P<revision_name>[\w\-]+)/data/(?P<data_name>[\w\-]+)/$', views.data, name='views.data'),
)


