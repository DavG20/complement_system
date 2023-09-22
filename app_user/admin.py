from django.contrib import admin

from complaints.models import Complaint

from .models import AppUser

# Register your models here.

admin.site.register(AppUser)
# admin.site.register(Complement)
