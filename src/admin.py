from django.contrib import admin


# Register your models here.
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Players
from .models import Matches
from .models import ClubAttendance
from .models import Updates

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Players)
admin.site.register(Matches)
admin.site.register(Updates)
admin.site.register(ClubAttendance)