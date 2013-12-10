# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: project.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 12.5.13
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from django.db import models
from django.contrib.auth.models import User

# App imports

# Main
class Project(models.Model):

    class Meta():
        app_label = 'socialnet'

    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    last_activity = models.DateTimeField()
    public = models.BooleanField()
    description = models.TextField(blank=True, null=True)

    # Relationships
    owner = models.ForeignKey(User, related_name='owned_project')
    contributor = models.ManyToManyField(User, blank=True, null=True, related_name='contributed_project')
    # added contributor -> not yet accepted
    observer = models.ManyToManyField(User, blank=True, null=True, related_name='watched_project')
    current_revision = models.OneToOneField('Revision', blank=True, null=True, related_name='active_project')

    def __unicode__(self):
        return self.name