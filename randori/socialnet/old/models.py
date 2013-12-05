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

    return os.path.join('photos/', str(instance.user.username) + '/', prepend + '/',   prepend + '__' + upload_time + '__' + filename)

def getDataPath(instance, filename):
    upload_time = str( datetime.datetime.now() )
    upload_time = upload_time.replace(' ', '_').replace('-', '_')

    return os.path.join('data/',  str(instance.owner.username) + '/',  str(instance.host.name) + '/', 'data__' + upload_time + '__' + filename)


# Models
class UserProfile(models.Model):
	# Attributes
    web_site = models.URLField(max_length=200, blank=True, null=True)
    profile_photo = models.ImageField(upload_to=getProfilePhotoPath, blank=True, null=True)
    cover_photo = models.ImageField(upload_to=getCoverPhotoPath, blank=True, null=True)
    bio = models.TextField(blank=True)

    # Relationships
    user = models.OneToOneField(User, related_name='additional_info')
    friend = models.ManyToManyField(User, blank=True, null=True)
    address = models.ManyToManyField('Address', related_name='lives')

    def __unicode__(self):
		return self.user.username

class Project(models.Model):
    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    last_activity = models.DateTimeField()
    public = models.BooleanField()
    description = models.TextField(blank=True, null=True)

    # Relationships
    owner = models.ForeignKey(User, related_name='owned_project')
    contributor = models.ManyToManyField(User, blank=True, null=True, related_name='contributed_project')
    observer = models.ManyToManyField(User, blank=True, null=True, related_name='watched_project')
    current_revision = models.OneToOneField('Revision', blank=True, null=True, related_name='active_project')

    def __unicode__(self):
        return self.name

class Revision(models.Model):
    # Attributes

    # Relationships
    # Add later tree
    # -> parent
    # -> children
    # Add later
    # -> owner
    version = models.ForeignKey('Version', related_name='in_revision')
    project = models.ForeignKey('Project', blank=True, null=True, related_name='previous_revision')
    software_stack = models.ManyToManyField('SoftwareStack', blank=True, null=True, related_name='used_for_revision')

    def __unicode__(self):
        return self.version.__unicode__()

    def name(self):
        return self.version.name()

    def dotName(self):
        return self.version.dotName()

class Version(models.Model):
    # Attributes
    major = models.PositiveIntegerField()
    minor = models.PositiveIntegerField()
    build = models.PositiveIntegerField()
    date_created = models.DateTimeField()
    last_activity = models.DateTimeField()

    # Relationships
    
    def __unicode__(self):
        return u'%s.%s.%s' % (str(self.major), str(self.minor), str(self.build))

    def ageComparison(self, other):
        pass

    def name(self):
        return '%s_%s_%s' % (str(self.major), str(self.minor), str(self.build))

    def dotName(self):
        return '%s.%s.%s' % (str(self.major), str(self.minor), str(self.build))

class Host(models.Model):
    # Attributes
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Relationships
    last_location = models.ForeignKey('Location', blank=True, null=True, related_name='current_host')

    def __unicode__(self):
        return self.name

class Data(models.Model):
    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    file_data = models.FileField(upload_to=getDataPath, blank=True, null=True)

    # Relationships
    owner = models.ForeignKey(User, related_name='collected_data')
    revision = models.ForeignKey('Revision', blank=True, null=True, related_name='collected_data')
    collected_location = models.ForeignKey('Location', blank=True, null=True, related_name='collected_data')
    host = models.ForeignKey('Host', blank=True, null=True, related_name='collected_data')

    def __unicode__(self):
        return self.name

class Location(models.Model):
    # Attributes
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    # Relationships
    sub_location = models.ManyToManyField("self", blank=True, null=True, related_name='parent_location')
    address = models.ForeignKey('Address', blank=True, null=True, related_name='location')

    def __unicode__(self):
        return self.name

class Address(models.Model):
    # Vars
    TYPE_CHOICES = ( ('HOME', 'home'),
                     ('WORK', 'work'),
                     ('OTHER', 'other'),)

    # Attributes
    address_type = models.CharField(max_length=200, choices=TYPE_CHOICES, default='text')
    address_1 = models.CharField(max_length=128, blank=True, null=True,)                                                           
    address_2 = models.CharField(max_length=128, blank=True, null=True,)  
    city = models.CharField(max_length=128)
    state = USStateField(US_STATES)                                                                                                                                           
    zipcode = models.CharField(max_length=5, blank=True, null=True,)                                                               
    zip_plus4 = models.CharField(max_length=4, blank=True, null=True,) 

    # Relationships

    def __unicode__(self):
        return '%s, %s' % (self.city, self.state)

class Analysis(models.Model):
    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    last_activity = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    # Relationships
    owner = models.ForeignKey(User, related_name='main_analysis')
    project = models.ForeignKey('Project', related_name='data_analysis')
    contributor = models.ManyToManyField(User, blank=True, null=True, related_name='contributed_analysis')
    data = models.ManyToManyField('Data', blank=True, null=True, related_name='data_analysis')

    def __unicode__(self):
        return self.name

class SoftwareStack(models.Model):
    # Attributes
    name = models.CharField(max_length=200)

    # Relationships
    version = models.ForeignKey(Version, related_name='in_software')
    dependency = models.ManyToManyField("self", blank=True, null=True, related_name='related_dependency')

    def __unicode__(self):
        return self.name
    



