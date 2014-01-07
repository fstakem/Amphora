from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
                       url(r'^/$', views.user, name='views.user'),
                       url(r'^/(?P<project_name>[\w\-]+)/$', views.project, name='views.project'),
                       url(r'^/(?P<project_name>[\w\-]+)/analysis/(?P<analysis_name>[\w\-]+)/$', views.analysis, name='views.analysis'),
)




