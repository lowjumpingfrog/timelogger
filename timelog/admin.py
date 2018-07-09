from django.contrib import admin
from import_export.resources import ModelResource
from import_export.admin import ExportMixin, ExportActionModelAdmin
from .models import TimeLog, Reasons, Facilities
from work_type.models import  WorkGroup, WorkCategory
from facilities.models import Facilities
from related_admin import RelatedFieldAdmin, getter_for_related_field
from import_export import fields, widgets
from django.contrib.auth.models import User
from rangefilter.filter import DateRangeFilter
from django.http import HttpResponse
from .utils import get_qgenda_shift, get_pay_record
import csv
import io


class TimeLogResource(ModelResource):

    user            = fields.Field(column_name = 'name', attribute='full_name') #fields.Field(column_name='user', attribute='user', widget=widgets.ForeignKeyWidget(User, 'username'))
    reason          = fields.Field(column_name='reason', attribute = 'reason', widget=widgets.ForeignKeyWidget(Reasons,'reason'))
    facility        = fields.Field(column_name='facility', attribute = 'facility', widget=widgets.ForeignKeyWidget(Facilities,'facility'))
    billable        = fields.Field(column_name='billable', attribute = 'reason', widget=widgets.ForeignKeyWidget(Reasons,'billable'))
    reconciled      = fields.Field(column_name='reconciled',attribute='reconciled')
    work_start_time = fields.Field(column_name='start',attribute='work_start_time')
    work_end_time   = fields.Field(column_name='end',attribute='work_end_time')
    duration        = fields.Field(attribute='duration')
    pay             = fields.Field(column_name = 'pay',attribute='pay')
    pay_memo        = fields.Field(column_name = 'memo', attribute='pay_memo')

    class Meta:
        model = TimeLog
        fields = ('user','facility','work_start_time','work_end_time', 'reason','shift','comment','duration','pay','pay_memo','reconciled','billable')
        export_order = ('user','facility','work_start_time','work_end_time', 'reason','shift','comment','duration','pay','pay_memo','reconciled','billable')
        readonly_fields = ('pay','pay_memo')

'''
def download_report(self, request, queryset):

    f = io.StringIO()
    writer = csv.writer(f)
    writer.writerow(["code", "country", "ip", "url", "count"])

    #for s in queryset:
        #writer.writerow([s.code, s.country, s.ip, s.url, s.count])

    f.close()
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=timelog_report.csv'
    return response

download_report.short_description = "Report on Selected Rows"'''

def set_reconciled(TimeLogAdmin,request,queryset):
	queryset.update(reconciled = 1)

set_reconciled.short_description = 'Set Reconciled'

def check_shifts(TimeLogAdmin,request,queryset):
    for i in range(len(queryset)):
        u_obj = User.objects.get(id = queryset[i].user_id)
        new_shift = get_qgenda_shift(u_obj.email,queryset[i].work_start_time.strftime('%m/%d/%Y'))
        TimeLog.objects.filter(id = queryset[i].id).update(shift = new_shift)


check_shifts.short_description = "Update Shifts"

def calculate_pay(TimeLogAdmin,request,queryset):
    for i in range(len(queryset)):
        pay_record = get_pay_record(queryset[i])
        TimeLog.objects.filter(id = queryset[i].id).update(pay = pay_record['pay'])
        TimeLog.objects.filter(id = queryset[i].id).update(pay_memo = pay_record['pay_memo'])

calculate_pay.short_description = 'Update Pay Fields'

def unset_reconciled(TimeLogAdmin,request,queryset):

	queryset.update(reconciled = 0)

unset_reconciled.short_description = 'Unset Reconciled'


class TimeLogAdmin(ExportMixin, RelatedFieldAdmin):
	ordering = ('-work_start_time',)
	search_fields = ['user__username','facility__facility','reason__reason','shift']
	list_filter = ( ('work_start_time', DateRangeFilter),
					('work_end_time', DateRangeFilter),
                    ('updated', DateRangeFilter),
					('reason__billable',admin.BooleanFieldListFilter),
					('reconciled',admin.BooleanFieldListFilter),
					('facility',admin.RelatedFieldListFilter)
				  )
	list_display = ('full_name','facility__facility','work_start_time','work_end_time','reason__reason','shift','comment','duration','pay','pay_memo','reconciled','reason__billable')
	actions = [set_reconciled,unset_reconciled,check_shifts,calculate_pay]
	resource_class = TimeLogResource


admin.site.register(TimeLog,TimeLogAdmin)
