# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: host.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 12.5.13
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from django.db import models

# App imports

# Main
class Host(models.Model):

    class Meta():
        app_label = 'socialnet'
        
    # Attributes
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Relationships
    last_location = models.ForeignKey('Location', blank=True, null=True, related_name='current_host')

    def __unicode__(self):
        return self.name