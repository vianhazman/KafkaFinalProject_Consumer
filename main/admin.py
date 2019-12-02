from django.contrib import admin

from .models import Bus
from .models import GpsPing

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    readonly_fields = ["bus_code","trip_id","koridor","timestamp_epoch"]

@admin.register(GpsPing)
class BusAdmin(admin.ModelAdmin):
    readonly_fields = ["bus_code","longitude","latitude","gps_timestamp"]