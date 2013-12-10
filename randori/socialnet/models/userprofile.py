# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: userprofile.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 12.5.13
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from django.db import models
from django.contrib.auth.models import User

# App imports
from helper import *

# Main
class UserProfile(models.Model):

    class Meta():
        app_label = 'socialnet'

    # Attributes
    web_site = models.URLField(max_length=200, blank=True, null=True)
    profile_photo = models.ImageField(upload_to=getProfilePhotoPath, blank=True, null=True)
    cover_photo = models.ImageField(upload_to=getCoverPhotoPath, blank=True, null=True)
    # title
    bio = models.TextField(blank=True)

    # Relationships
    user = models.OneToOneField(User, related_name='additional_info')
    friend = models.ManyToManyField(User, blank=True, null=True)
    address = models.ManyToManyField('Address', related_name='lives')

    def __unicode__(self):
        return self.user.username
