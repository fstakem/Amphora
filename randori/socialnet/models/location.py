# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: location.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 12.5.13
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from django.db import models

# App imports

# Main
class Location(models.Model):

    class Meta():
        app_label = 'socialnet'

    # Attributes
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    # Relationships
    sub_location = models.ManyToManyField("self", blank=True, null=True, related_name='parent_location')
    address = models.ForeignKey('Address', blank=True, null=True, related_name='location')

    def __unicode__(self):
        return self.name