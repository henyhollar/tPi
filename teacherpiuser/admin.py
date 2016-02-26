from django.contrib import admin

from .models import TeacherPiUser, MacAddress, DefaultPass
# Register your models here.
admin.site.register(TeacherPiUser)
admin.site.register(MacAddress)
admin.site.register(DefaultPass)
