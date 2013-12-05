# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: data.py
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
class Data(models.Model):

    class Meta():
        app_label = 'socialnet'

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