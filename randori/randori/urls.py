from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Social auth
    url('', include('social.apps.django_app.urls', namespace='social'))
)
