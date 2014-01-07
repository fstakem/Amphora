# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: dataset.py
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
class DataSet(models.Model):

    class Meta():
        app_label = 'socialnet'

    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)

    # Relationships
    project = models.ForeignKey('DataSet', related_name='data_set')
    creator = models.ForeignKey(User, related_name='data_set')

    def __unicode__(self):
        return self.name