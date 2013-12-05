# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: softwarestack.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 12.5.13
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from django.db import models

# App imports

# Main
class SoftwareStack(models.Model):

    class Meta():
        app_label = 'socialnet'

    # Attributes
    name = models.CharField(max_length=200)

    # Relationships
    version = models.ForeignKey('Version', related_name='in_software')
    dependency = models.ManyToManyField("self", blank=True, null=True, related_name='related_dependency')

    def __unicode__(self):
        return self.name
