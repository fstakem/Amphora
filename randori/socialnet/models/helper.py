# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: helper.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 12.5.13
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys
import os
import datetime

# App imports

# Main
def getCoverPhotoPath(instance, filename):
    return getImagePath(instance, filename, 'cover')

def getProfilePhotoPath(instance, filename):
    return getImagePath(instance, filename, 'profile')

def getImagePath(instance, filename, prepend): 
    if len(prepend) == 0:
        prepend = 'generic'

    upload_time = str( datetime.datetime.now() )
    upload_time = upload_time.replace(' ', '_').replace('-', '_')

    return os.path.join('photos/', str(instance.user.username) + '/', prepend + '/',   prepend + '__' + upload_time + '__' + filename)

def getDataPath(instance, filename):
    upload_time = str( datetime.datetime.now() )
    upload_time = upload_time.replace(' ', '_').replace('-', '_')

    return os.path.join('data/',  str(instance.owner.username) + '/',  str(instance.host.name) + '/', 'data__' + upload_time + '__' + filename)