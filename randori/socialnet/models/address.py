# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: address.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 12.5.13
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from django.db import models
from localflavor.us.models import USStateField
from localflavor.us.us_states import US_STATES

# App imports

# Main
class Address(models.Model):

    class Meta():
        app_label = 'socialnet'

    # Vars
    TYPE_CHOICES = ( ('HOME', 'home'),
                     ('WORK', 'work'),
                     ('OTHER', 'other'),)

    # Attributes
    address_type = models.CharField(max_length=200, choices=TYPE_CHOICES, default='text')
    address_1 = models.CharField(max_length=128, blank=True, null=True,)                                                           
    address_2 = models.CharField(max_length=128, blank=True, null=True,)  
    city = models.CharField(max_length=128)
    state = USStateField(US_STATES)                                                                                                                                           
    zipcode = models.CharField(max_length=5, blank=True, null=True,)                                                               
    zip_plus4 = models.CharField(max_length=4, blank=True, null=True,) 

    # Relationships

    def __unicode__(self):
        return '%s, %s' % (self.city, self.state)