from django.contrib import admin
from .models import Room, ApplianceCategory, Appliance, AirConditioner

admin.site.register(Room)
admin.site.register(ApplianceCategory)
admin.site.register(Appliance)
admin.site.register(AirConditioner)
