# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: analysis.py
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
class Analysis(models.Model):

    class Meta():
        app_label = 'socialnet'

    # Attributes
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    last_activity = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    # Relationships
    owner = models.ForeignKey(User, related_name='main_analysis')
    project = models.ForeignKey('Project', related_name='data_analysis')
    contributor = models.ManyToManyField(User, blank=True, null=True, related_name='contributed_analysis')
    data = models.ManyToManyField('Data', blank=True, null=True, related_name='data_analysis')

    def __unicode__(self):
        return self.name