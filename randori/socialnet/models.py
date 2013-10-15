import os
import datetime

from django.db import models
from localflavor.us.models import USStateField
from localflavor.us.us_states import US_STATES
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
    bio = models.TextField(blank=True)

    # Relationships
    user = models.OneToOneField(User, related_name='additional_info')
    friend = models.ForeignKey("self", blank=True)
    address = models.ManyToManyField('Address', related_name='lives')

    def __unicode__(self):
		return self.user.username

class Project(models.Model):
    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    last_activity = models.DateTimeField()
    public = models.BooleanField()
    description = models.TextField(blank=True)

    # Relationships
    owner = models.ForeignKey('UserProfile', related_name='owned_project')
    contributor = models.ManyToManyField('UserProfile', related_name='contributed_project')
    observer = models.ManyToManyField('UserProfile', related_name='watched_project')
    current_revision = models.OneToOneField('Revision', related_name='active_project')

    def __unicode__(self):
        return self.name

class Revision(models.Model):
    # Attributes

    # Relationships
    version = models.ForeignKey('Version', related_name='in_revision')
    host = models.ManyToManyField('Host', related_name='in_revision')
    project = models.ForeignKey('Project', related_name='previous_revision')
    software_stack = models.ForeignKey('SoftwareStack', related_name='used_for_revision')

    def __unicode__(self):
        return str(self.version)

    def ageComparison(self, other):
        pass

class Version(models.Model):
    # Attributes
    major = models.PositiveIntegerField()
    minor = models.PositiveIntegerField()
    build = models.PositiveIntegerField()
    date_created = models.DateTimeField()
    last_activity = models.DateTimeField()

    # Relationships
    
    def __unicode__(self):
        return str(self.major) + '.' + str(self.minor) + '.' + str(self.build)

    def ageComparison(self, other):
        pass

class Host(models.Model):
    # Attributes
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Relationships
    last_location = models.ForeignKey('Location', related_name='current_host')

    def __unicode__(self):
        return self.name

class Data(models.Model):
    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    description = models.TextField(blank=True)
    file_data = models.FileField(upload_to=getDataPath, blank=True, null=True)

    # Relationships
    owner = models.ForeignKey('UserProfile', related_name='collected_data')
    location = models.ForeignKey('Location', related_name='collected_data')
    host = models.ForeignKey('Host', related_name='collected_data')

    def __unicode__(self):
        return self.name

class Location(models.Model):
    # Attributes
    name = models.CharField(max_length=200)

    # Relationships
    sub_location = models.ForeignKey("self", related_name='parent_location', blank=True)
    address = models.ForeignKey('Address', related_name='location', blank=True)

    def __unicode__(self):
        return self.name

class Address(models.Model):
    # Attributes
    address_type = models.CharField(max_length=200)
    address_1 = models.CharField(max_length=128, blank=True)                                                           
    address_2 = models.CharField(max_length=128, blank=True)  
    city = models.CharField(max_length=128)
    state = USStateField(US_STATES)                                                                                                                                           
    zipcode = models.CharField(max_length=5, blank=True)                                                               
    zip_plus4 = models.CharField(max_length=4, blank=True) 

    # Relationships

    def __unicode__(self):
        return self.city + ', ' + self.state

class Analysis(models.Model):
    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    last_activity = models.DateTimeField()
    description = models.TextField(blank=True)

    # Relationships
    owner = models.ForeignKey('UserProfile', related_name='main_analysis')
    contributor = models.ManyToManyField('UserProfile', related_name='contributed_analysis')
    revision = models.ForeignKey('Revision', related_name='data_analysis')
    data = models.ManyToManyField('Data', related_name='data_analysis')

    def __unicode__(self):
        return self.name

class SoftwareStack(models.Model):
    # Attributes
    name = models.CharField(max_length=200)

    # Relationships
    version = models.ForeignKey(Version, related_name='in_software')

    def __unicode__(self):
        return self.name
    



