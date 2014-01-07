# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++
# 
#       File: helper.py
#       By: Fred Stakem
#       For: Private Research
#       Date: 12.5.13
#
# +++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++---+++


# Librarys

# App imports

# Main
def isUsersPageAndLoggedIn(viewer, user_to_be_viewed):
    if viewer.is_authenticated() and viewer.username == user_to_be_viewed.username:
        return True
    else:
        return False