# Django settings for randori project.

# Project directories
import os

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
SITE_ROOT = PROJECT_ROOT + '/..'
SCM_ROOT = SITE_ROOT + '/..'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'randori', 
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',                      
        'PORT': '5432',                      
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

FILE_UPLOAD_PERMISSIONS = 0644

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static_coll')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'p5=o*p^j@45j=_dyhol%+6zwn1khlkg^cwt&h9)s2vm8=9u)%^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'randori.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'randori.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # 'django.contrib.admindocs',

    # User apps
    'socialnet',

    # Python social auth
    'social.apps.django_app.default',

    # Bootstrap integration
    #'bootstrap3',

    # Crispy forms integration
    'crispy_forms',

    # Local 
    'localflavor',

    # tagging
    'taggit',

    # command extensions
    'django_extensions',
)

AUTHENTICATION_BACKENDS = (
      'social.backends.open_id.OpenIdAuth',
      'social.backends.google.GoogleOpenId',
      'social.backends.google.GoogleOAuth2',
      'social.backends.google.GoogleOAuth',
      'social.backends.github.GithubOAuth2',
      'django.contrib.auth.backends.ModelBackend',
  )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# START: For Heroku
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config(default='postgres://localhost/randori')

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# END: For Heroku
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# START: For Crispy Forms
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
CRISPY_TEMPLATE_PACK = 'bootstrap3'
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# END: For Crispy Forms
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# START: For django-extension graphviz
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# END: For django-extension graphviz
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# START: For python-social-auth
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

LOGIN_ERROR_URL = ''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# END: For python-social-auth
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++