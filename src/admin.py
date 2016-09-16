from django.contrib import admin


# Register your models here.
from .models import Players
from .models import Matches

admin.site.register(Players)
admin.site.register(Matches)
