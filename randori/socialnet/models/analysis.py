# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: analysis.py
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
class Analysis(models.Model):

    class Meta():
        app_label = 'socialnet'

    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    tags = TaggableManager(blank=True)

    # Relationships
    creator = models.ForeignKey(User, related_name='analysis')
    project = models.ForeignKey('Project', related_name='analysis')
    data = models.ManyToManyField('Data', blank=True, null=True, related_name='analysis')

    def __unicode__(self):
        return self.name