# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: project.py
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

# Main
class Project(models.Model):

    class Meta():
        app_label = 'socialnet'

    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    public = models.BooleanField()
    description = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    tags = TaggableManager(blank=True)

    # Relationships
    owner = models.ForeignKey(User, related_name='owned_project')
    contributor = models.ManyToManyField(User, blank=True, null=True, related_name='contributed_project')
    pending_contributor = models.ManyToManyField(User, blank=True, null=True, related_name='pending_contributed_project')
    host = models.ManyToManyField('Host', blank=True, null=True, related_name='project')

    def __unicode__(self):
        return self.name