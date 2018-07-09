from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, ButtonHolder, HTML, Button, Fieldset
from datetimewidget.widgets import DateTimeWidget, DateWidget
#https://github.com/asaglimbeni/django-datetime-widget
#from crispy_forms.bootstrap import PrependedText, PrependedAppendedText, FormActions
import datetime
from datetime import timedelta
from .models import TimeLog
from reasons.models import Reasons
from .utils import calculate_duration

class TimeLogReportForm(forms.Form):
	report_start = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
	report_end = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))

	def clean(self):
		cleaned_data = super(TimeLogReportForm,self).clean()

		# check time entry order
		report_start = cleaned_data.get('report_start')
		report_end = cleaned_data.get('report_end')

		if report_start > report_end:
			raise forms.ValidationError("Start time has to be before End Time.")

	def __init__(self, *args, **kwargs):
	    self.helper = FormHelper()
	    self.helper.form_id = 'id-TimeLogReportForm'
	    self.helper.form_class = 'form-horizontal'
	    self.helper.form_method = 'post'
	    self.helper.form_action = 'report_view'

	    self.helper.add_input(Submit('submit', 'Submit'))
	    super(TimeLogReportForm, self).__init__(*args, **kwargs)


class TimeLogForm(forms.ModelForm):
	class Meta:
		model = TimeLog
		fields = [
			'reason',
			'facility',
			'work_start_time',
			'work_end_time',
			'comment',
		]
		dateTimeOptions = {
			'format': 'mm/dd/yyyy HH:ii P',
			'autoclose': True,
			'showMeridian' : True,
			'pickerPosition' : 'bottom-left',
			'minuteStep' : 5,
		}
		widgets = {
            #Use localization and bootstrap 3
            'work_start_time': DateTimeWidget(attrs={'id':"work_start_time",'readonly':"true"}, usel10n = True, bootstrap_version=3, options=dateTimeOptions),
            'work_end_time': DateTimeWidget(attrs={'id':"work_end_time",'readonly':"true"}, usel10n = True, bootstrap_version=3, options=dateTimeOptions)
        }

	def clean(self):
		cleaned_data = super(TimeLogForm,self).clean()
		reason_check = Reasons.objects.get(reason = cleaned_data['reason'])

		#check for needed comment
		if reason_check.comment_needed and cleaned_data.get('comment') == None:
			raise forms.ValidationError("This reason needs a meaningful comment.")

		# check time entry order
		start_time = cleaned_data.get('work_start_time')
		stop_time = cleaned_data.get('work_end_time')
		if start_time > stop_time:
			raise forms.ValidationError("Start time has to be before End Time.")

		# check for max time
		if (stop_time - start_time)/timedelta(hours=1) > reason_check.max_time:
		 	raise forms.ValidationError("Submission for this reason is limited to " + str(reason_check.max_time) + " hours.")

		# Check for overlapping entries
		start_check = TimeLog.objects.filter(user__username=self.user).filter(work_start_time__range=[start_time,stop_time])
		stop_check = TimeLog.objects.filter(user__username=self.user).filter(work_end_time__range=[start_time,stop_time])

		message = 'good'

		for row in start_check:
			time_diff = calculate_duration(start_time,stop_time,row.work_start_time,row.work_end_time)
			if time_diff > 0:
				message = "Time entry overlap, you have an entry that starts: " + str(row.work_start_time) + " and ends: " + str(row.work_end_time)
				break
		if message != 'good':
			raise forms.ValidationError(message)

		for row in stop_check:
			time_diff = calculate_duration(start_time,stop_time,row.work_start_time,row.work_end_time)
			if time_diff > 0:
				message = "Time entry overlap, you have an entry that starts: " + str(row.work_start_time) + " and ends: " + str(row.work_end_time)
				break

		if message != 'good':
			raise forms.ValidationError(message)

		# check for duplicates
		user = cleaned_data.get('user')
		reason = cleaned_data.get('reason')
		facility = cleaned_data.get('facility')
		work_start_time = cleaned_data.get('work_start_time')
		work_end_time = cleaned_data.get('work_end_time')
		test = TimeLog.objects.filter(reason = reason,
								facility = facility,
								work_start_time = start_time,
								work_end_time = stop_time).exists()
		if test:
			raise forms.ValidationError('Duplicate Entry')

	def __init__(self, user=None, *args, **kwargs):
		self.user = user
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		self.helper.layout = Layout(
		    Div(
		    Fieldset(
		        'Time record for {{ user.username }}:',
		        'reason',
		        'facility',
		        'work_start_time',
		        'work_end_time',
		        'comment',
		    ),
		    ButtonHolder(
    			Submit('Save', 'Save', css_class='button white'),
    			HTML('<a class="btn btn-warning" href={% url "home" %}>Cancel</a>'),
				HTML("""{% if object %}
                <a href="{% url "timelog:delete" object.id %}"
                class="btn btn-outline-danger">
                <h3 class="glyphicon glyphicon-trash"></h3></button></a>
                {% endif %}"""),
			),
		    css_class='col-md-12'
		    )
		)
		self.request = kwargs.pop('request', None)
		super(TimeLogForm, self).__init__(*args, **kwargs)
		#get the users group id
		#group_id = user.groups.values_list('id', flat=True).first()
		#self.fields['reason'].queryset = Reasons.objects.filter(group_id=group_id).order_by('reason')
