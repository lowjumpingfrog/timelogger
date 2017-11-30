from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, ButtonHolder, HTML, Button, Fieldset
from datetimewidget.widgets import DateTimeWidget
#https://github.com/asaglimbeni/django-datetime-widget
#from crispy_forms.bootstrap import PrependedText, PrependedAppendedText, FormActions
import datetime

from .models import TimeLog


class TimeLogForm(forms.ModelForm):
	class Meta:
		model = TimeLog
		fields = [
			'category',
			'work_start_time',
			'work_end_time',
			'comment',
		]
		dateTimeOptions = {
			'format': 'dd/mm/yyyy HH:ii',
			'autoclose': True,
			'showMeridian' : True,
			'pickerPosition' : 'bottom-left',
			'minuteStep' : 30,
			'endDate':  str(datetime.datetime.today().date())
		}
		widgets = {
            #Use localization and bootstrap 3
            'work_start_time': DateTimeWidget(attrs={'id':"work_start_time"}, usel10n = True, bootstrap_version=3, options=dateTimeOptions),
            'work_end_time': DateTimeWidget(attrs={'id':"work_start_time"}, usel10n = True, bootstrap_version=3, options=dateTimeOptions)
        }


	def __init__(self, user=None, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_class = 'form-horizontal'
		
		self.helper.layout = Layout(
		    Div(
		    Fieldset(
		        'Time record for {{ user.username }}:',
		        'category',
		        'work_start_time',
		        'work_end_time',
		        'comment',
		    ),
		    ButtonHolder(
    			Submit('Save', 'Save', css_class='button white'),
    			HTML('<a class="btn btn-warning" href={% url "home" %}>Cancel</a>'),
			),
		    css_class='col-md-12'
		    )
		)

		self.request = kwargs.pop('request', None)
		return super(TimeLogForm, self).__init__(*args, **kwargs)		

		