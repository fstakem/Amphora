# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: version.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 12.5.13
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from django.db import models

# App imports

# Main
class Version(models.Model):

    class Meta():
        app_label = 'socialnet'
        
    # Attributes
    major = models.PositiveIntegerField()
    minor = models.PositiveIntegerField()
    build = models.PositiveIntegerField()
    date_created = models.DateTimeField()
    last_activity = models.DateTimeField()

    # Relationships
    
    def __unicode__(self):
        return u'%s.%s.%s' % (str(self.major), str(self.minor), str(self.build))

    def ageComparison(self, other):
        pass

    def name(self):
        return '%s_%s_%s' % (str(self.major), str(self.minor), str(self.build))

    def dotName(self):
        return '%s.%s.%s' % (str(self.major), str(self.minor), str(self.build))