from django.contrib import admin
from socialnet.models import UserProfile, Project, Revision, Version, Host, Data, Location, Address, Analysis, SoftwareStack

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Revision)
admin.site.register(Version)
admin.site.register(Host)
admin.site.register(Data)
admin.site.register(Location)
admin.site.register(Address)
admin.site.register(Analysis)
admin.site.register(SoftwareStack)