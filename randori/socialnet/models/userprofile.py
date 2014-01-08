# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: userprofile.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 1.7.14
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
    personal_website = models.URLField(max_length=200, blank=True, null=True)
    github_page = models.URLField(max_length=200, blank=True, null=True)
    profile_photo = models.ImageField(upload_to=getProfilePhotoPath, blank=True, null=True)
    cover_photo = models.ImageField(upload_to=getCoverPhotoPath, blank=True, null=True)
    title = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now_add=True)

    # Relationships
    location = models.ForeignKey('Location', related_name='user_live_here')
    user = models.OneToOneField(User, related_name='additional_info')
    followed = models.ManyToManyField(User, blank=True, null=True, related_name='follower')

    def __unicode__(self):
        return self.user.username
