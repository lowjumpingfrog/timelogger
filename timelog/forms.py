from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, ButtonHolder, HTML, Button, Fieldset
from datetimewidget.widgets import DateTimeWidget
#https://github.com/asaglimbeni/django-datetime-widget
#from crispy_forms.bootstrap import PrependedText, PrependedAppendedText, FormActions
import datetime
from datetime import timedelta

from .models import TimeLog
from reasons.models import Reasons


class TimeLogForm(forms.ModelForm):
	class Meta:
		model = TimeLog
		fields = [
			'reason',
			'facility',
			'work_start_time',
			'work_end_time',
			'comment',
			'billable',
		]
		dateTimeOptions = {
			'format': 'dd/mm/yyyy HH:ii',
			'autoclose': True,
			'showMeridian' : True,
			'pickerPosition' : 'bottom-left',
			'minuteStep' : 15,
			'endDate':  str(datetime.date.today()+datetime.timedelta(days=1))
		}
		widgets = {
            #Use localization and bootstrap 3
            'work_start_time': DateTimeWidget(attrs={'id':"work_start_time",'readonly':"true"}, usel10n = True, bootstrap_version=3, options=dateTimeOptions),
            'work_end_time': DateTimeWidget(attrs={'id':"work_start_time",'readonly':"true"}, usel10n = True, bootstrap_version=3, options=dateTimeOptions)
        }

	def clean(self):
		cleaned_data = super(TimeLogForm,self).clean()
		start_time = cleaned_data.get('work_start_time')
		stop_time = cleaned_data.get('work_end_time')
		
		if start_time > stop_time:
			raise forms.ValidationError("Start time has to be before End Time.")

		if (stop_time - start_time)/timedelta(hours=1) > 24:
		 	raise forms.ValidationError("Submissions longer than 24 hours not allowed.")
	
	def __init__(self, user=None, *args, **kwargs):
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
		        'billable',
		    ),
		    ButtonHolder(
    			Submit('Save', 'Save', css_class='button white'),
    			HTML('<a class="btn btn-warning" href={% url "home" %}>Cancel</a>'),
			),
		    css_class='col-md-12'
		    )
		)
		self.request = kwargs.pop('request', None)
		super(TimeLogForm, self).__init__(*args, **kwargs)
		#get the users group id
		group_id = user.groups.values_list('id', flat=True).first()
		self.fields['reason'].queryset = Reasons.objects.filter(group_id=group_id).order_by('reason')

		