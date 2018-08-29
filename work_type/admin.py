from django.contrib import admin
from .models import WorkCategory, WorkGroup

class WorkGroupAdmin(admin.ModelAdmin):
    fields = ['name', 'timestamp', 'updated']

class WorkCategoryAdmin(admin.ModelAdmin):
    list_display =  ('work_category', 'start_time', 'stop_time', 'points_per_hr','rate')
    readonly_fields = ('rate',)

# Register your models here.
admin.site.register(WorkCategory,WorkCategoryAdmin)
#admin.site.register(WorkCategoryAdmin)
admin.site.register(WorkGroup)
