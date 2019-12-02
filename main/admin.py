from django.contrib import admin

from .models import Bus
from .models import GpsPing


admin.site.register(Bus)
admin.site.register(GpsPing)