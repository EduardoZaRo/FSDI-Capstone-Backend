from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin


# @admin.register(get_user_model())
# class CustomUserAdmin(UserAdmin):
#     pass
# Register your models here.
admin.site.register(Microcontroller)
admin.site.register(Peripheral)
admin.site.register(Device)
admin.site.register(User)
admin.site.register(Read)
admin.site.register(Action)
admin.site.register(DevicePeripheral)