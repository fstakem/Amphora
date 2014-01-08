# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: location.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 1.7.14
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from django.db import models

from taggit.managers import TaggableManager

# App imports

# Main
class Location(models.Model):

    class Meta():
        app_label = 'socialnet'

    # Attributes
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=128)                                                                                                                                         
    description = models.TextField(blank=True, null=True)
    tags = TaggableManager(blank=True)

    # Relationships

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.city)