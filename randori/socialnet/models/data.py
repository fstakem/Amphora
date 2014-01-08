# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: data.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 1.7.14
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

# App imports
from helper import *

# Main
class Data(models.Model):

    class Meta():
        app_label = 'socialnet'

    # Attributes
    name = models.CharField(max_length=200)
    date_started_collection = models.DateTimeField()
    date_ended_collection = models.DateTimeField()
    date_uploaded = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    raw_data = models.FileField(upload_to=getDataPath, blank=True, null=True)
    tags = TaggableManager(blank=True)

    # Relationships
    owner = models.ForeignKey(User, related_name='collected_data')
    project = models.ForeignKey('Project', related_name='data')
    location = models.ForeignKey('Location', blank=True, null=True, related_name='collected_data')
    host = models.ForeignKey('Host', blank=True, null=True, related_name='collected_data')

    def __unicode__(self):
        return self.name