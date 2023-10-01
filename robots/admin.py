from django.contrib import admin
from .models import Robot

# Register your models here.
@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
   list_display = ["model", "version", "serial", "created"]