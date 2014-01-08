# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: user.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 1.7.14
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
from django.contrib.auth.models import User
from django.http import HttpResponse

# App imports
from ..models import UserProfile, Project, Analysis, Data, Location, Host
from helper import isUsersPageAndLoggedIn

# Main
def user(request, user_name):
    return HttpResponse(status=404)