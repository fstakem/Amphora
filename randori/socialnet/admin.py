from django.contrib import admin
from socialnet.models import UserProfile, Project, Host, DataSet, Data, Location, Analysis

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Host)
admin.site.register(DataSet)
admin.site.register(Data)
admin.site.register(Location)
admin.site.register(Analysis)
