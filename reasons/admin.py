from django.contrib import admin
from .models import Reasons
# Register your models here.
class ReasonsAdmin(admin.ModelAdmin):
    list_display =  ('reason', 'billable', 'group', 'max_time','comment_needed')

admin.site.register(Reasons,ReasonsAdmin)
