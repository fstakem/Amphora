from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = patterns('',
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Social auth
    url('', include('social.apps.django_app.urls', namespace='social')),

    # Landing
    url(r'^$', views.landing, name='randori.views.landing'),

    # Misc
    url(r'^features$', views.features, name='randori.views.features'),
    url(r'^blog$', views.blog, name='randori.views.blog'),
    url(r'^terms$', views.terms, name='randori.views.terms'),
    url(r'^privacy$', views.privacy, name='randori.views.privacy'),
    url(r'^about$', views.about, name='randori.views.about'),
    url(r'^contact$', views.contact, name='randori.views.contact'),

    # Authentication
    url(r'^login$', views.login, name='randori.views.login'),
    url(r'^authentication$', views.authentication, name='randori.views.authentication'),
    url(r'^logout$', views.logout, name='randori.views.logout'),
    url(r'^register$', views.register, name='randori.views.register'),

    # Users
    url(r'^(?P<user_name>[\w\-]+)', include('socialnet.urls')),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
