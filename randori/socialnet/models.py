import os

from django.db import models
from django.contrib.auth.models import User

# Helper functions
def getCoverPhotoPath(instance, filename):
    getImagePath(instance, filename, 'cover')

def getProfilePhotoPath(instance, filename):
    getImagePath(instance, filename, 'profile')

def getImagePath(instance, filename, prepend):
    if len(prepend) > 0:
        prepend = prepend + '_'
    return os.path.join('photos', prepend + str(instance.user.username), filename)

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

    # Relationships
    owner = models.ForeignKey(User, related_name='owned_project')
    contributor = models.ManyToManyField(User, related_name='contributed_project')

    def __unicode__(self):
        return self.name

