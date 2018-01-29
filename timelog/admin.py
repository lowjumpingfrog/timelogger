from django.contrib import admin
from import_export.resources import ModelResource
from import_export.admin import ExportMixin, ExportActionModelAdmin
from .models import TimeLog, Reasons, Facilities
from related_admin import RelatedFieldAdmin, getter_for_related_field
from import_export import fields, widgets
from django.contrib.auth.models import User

'''class TimeLogAdmin(RelatedFieldAdmin):
	list_display = ('user__last_name','facility__facility','work_start_time','work_end_time', 'reason__reason','shift','reconciled','billable') 

admin.site.register(TimeLog,TimeLogAdmin)'''

class TimeLogResource(ModelResource):

    user = fields.Field(column_name='user', attribute='user', widget=widgets.ForeignKeyWidget(User, 'username'))
    reason = fields.Field(column_name='reason', attribute = 'reason', widget=widgets.ForeignKeyWidget(Reasons,'reason'))
    facility = fields.Field(column_name='facility', attribute = 'facility', widget=widgets.ForeignKeyWidget(Facilities,'facility'))
    #reconciled = fields.Field(widget=widgets.BooleanWidget())
    #billable = fields.Field(widget=widgets.BooleanWidget())

    #def for_reconciled(self, row, instance):
    #            return self.fields['reconciled'].render(row)

    #def for_billable(self, row, instance):
    #    return self.fields['billable'].render(row)

    class Meta:
        model = TimeLog
        fields = ('user','facility','work_start_time','work_end_time', 'reason','shift','reconciled','billable')
        export_order = ('user','facility','work_start_time','work_end_time', 'reason','shift','reconciled','billable')

class TimeLogAdmin(ExportMixin, RelatedFieldAdmin):
    #list_display = ('reason','facility')
    list_display = ('user__username','facility__facility','work_start_time','work_end_time', 'reason__reason','shift','reconciled','billable') 
    resource_class = TimeLogResource

admin.site.register(TimeLog,TimeLogAdmin)

#