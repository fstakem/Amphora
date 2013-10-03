from django.contrib import admin
from socialnet.models import UserProfile, Project, Data, Analysis

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Data)
admin.site.register(Analysis)