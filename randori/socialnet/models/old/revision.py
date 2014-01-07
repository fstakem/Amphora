# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: revision.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 12.5.13
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from django.db import models

# App imports

# Main
class Revision(models.Model):

    class Meta():
        app_label = 'socialnet'
        
    # Attributes

    # Relationships
    # Add later tree
    # -> parent
    # -> children
    # Add later
    # -> owner
    version = models.ForeignKey('Version', related_name='in_revision')
    project = models.ForeignKey('Project', blank=True, null=True, related_name='previous_revision')
    software_stack = models.ManyToManyField('SoftwareStack', blank=True, null=True, related_name='used_for_revision')

    def __unicode__(self):
        return self.version.__unicode__()

    def name(self):
        return self.version.name()

    def dotName(self):
        return self.version.dotName()