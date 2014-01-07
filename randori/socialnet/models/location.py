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

# App imports

# Main
class Location(models.Model):

    class Meta():
        app_label = 'socialnet'

    # Attributes
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    # Relationships

    def __unicode__(self):
        return self.name