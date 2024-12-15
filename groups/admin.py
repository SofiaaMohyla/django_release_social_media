from django.contrib import admin
from groups.models import Group, Member, Channel, Viewer

# Register your models here.

admin.site.register(Group)
admin.site.register(Member)
admin.site.register(Channel)
admin.site.register(Viewer)