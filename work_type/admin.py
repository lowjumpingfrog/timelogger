from django.contrib import admin
from .models import WorkCategory, WorkGroup

class WorkGroupAdmin(admin.ModelAdmin):
    fields = ['name', 'timestamp', 'updated']

class WorkCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'group', 'start_time', 'stop_time', 'points_per_hr', 'daytime_rate_factor', 'rate', 'timestamp', 'updated']

# Register your models here.
admin.site.register(WorkCategory)
admin.site.register(WorkGroup)
