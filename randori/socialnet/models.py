import os
import datetime

from django.db import models
from django.contrib.auth.models import User

# Helper functions
def getCoverPhotoPath(instance, filename):
    return getImagePath(instance, filename, 'cover')

def getProfilePhotoPath(instance, filename):
    return getImagePath(instance, filename, 'profile')

def getImagePath(instance, filename, prepend): 
    if len(prepend) == 0:
        prepend = 'generic'

    upload_time = str( datetime.datetime.now() )
    upload_time = upload_time.replace(' ', '_').replace('-', '_')

    return os.path.join('photos/', prepend + '/',  str(instance.user.username) + '/', prepend + '__' + upload_time + '__' + filename)

def getDataPath(instance, filename):
    upload_time = str( datetime.datetime.now() )
    upload_time = upload_time.replace(' ', '_').replace('-', '_')

    return os.path.join('data/project/',  str(instance.project.name) + '/',  'data__' + upload_time + '__' + filename)

# Models
class UserProfile(models.Model):
	# Attributes
    web_site = models.URLField(max_length=200, blank=True)
    profile_photo = models.ImageField(upload_to=getProfilePhotoPath, blank=True, null=True)
    cover_photo = models.ImageField(upload_to=getCoverPhotoPath, blank=True, null=True)

    # Relationships
    user = models.OneToOneField(User)
    friend = models.ManyToManyField(User, related_name='friend', blank=True)

    def __unicode__(self):
		return self.user.username

class Project(models.Model):
    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    last_activity = models.DateTimeField()
    public = models.BooleanField()
    description = models.CharField(max_length=200)

    # Relationships
    owner = models.ForeignKey(User, related_name='owned_project')
    contributor = models.ManyToManyField(User, related_name='contributed_project')

    def __unicode__(self):
        return self.name

class Data(models.Model):
    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    description = models.CharField(max_length=200)
    file_data = models.FileField(upload_to=getDataPath, blank=True, null=True)

    # Relationships
    owner = models.ForeignKey(User, related_name='owned_data')
    project = models.ForeignKey(Project, related_name='contained_data')

    def __unicode__(self):
        return self.name

class Analysis(models.Model):
    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    last_activity = models.DateTimeField()
    description = models.CharField(max_length=200)

    # Relationships
    owner = models.ForeignKey(User, related_name='owned_analysis')
    contributor = models.ManyToManyField(User, related_name='contributed_analysis')
    project = models.ForeignKey(Project, related_name='contained_analysis')

    def __unicode__(self):
        return self.name

