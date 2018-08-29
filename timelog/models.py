from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from work_type.models import WorkCategory
from reasons.models import Reasons
from facilities.models import Facilities
from .utils import get_qgenda_shift, calculate_pay_window, calculate_duration
from time import strftime
from django.conf import settings
from django.db.models import Q
from .utils import get_pay_record


User = settings.AUTH_USER_MODEL


class TimeLog(models.Model):
	user			= models.ForeignKey(User,on_delete=models.DO_NOTHING)
	reason			= models.ForeignKey(Reasons,on_delete=models.DO_NOTHING,verbose_name='Reason')
	facility		= models.ForeignKey(Facilities,on_delete=models.DO_NOTHING,verbose_name='Facility')
	work_start_time	= models.DateTimeField(auto_now=False, auto_now_add=False,verbose_name='Work Start Time')
	work_end_time	= models.DateTimeField(auto_now=False, auto_now_add=False,verbose_name='Work End Time')
	comment 		= models.CharField(max_length=512, null=True,blank=True,verbose_name='Comment')
	shift 			= models.CharField(max_length=255, null=True,blank=True,verbose_name='Shift')
	reconciled		= models.BooleanField(default=False,verbose_name='Is Reconciled')
	pay_memo		= models.CharField(max_length=512, null=True,blank=True,verbose_name='Memo')
	pay				= models.DecimalField(null=True, blank=True, max_digits=10,decimal_places=2)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True,verbose_name='Entry Date')

	class Meta:
		unique_together = ["user","reason","facility","work_start_time","work_end_time"]

	def __str__(self):
		return self.user.username + ' - ' + self.work_start_time.strftime('%m/%d/%Y')

	def get_email(self):
		return self.user.email

	def _get_full_name(self):
		"Returns the person's full name."
		return '%s, %s' % (self.user.last_name, self.user.first_name)

	full_name = property(_get_full_name)

	def _get_duration(self):
		"Computes the difference of work_end_time and work_start_time"
		delta = self.work_end_time - self.work_start_time
		hours, remainder = divmod(delta.total_seconds(), 3600)
		minutes, seconds = divmod(remainder, 60)
		return '%sh : %sm' % ('{:0>2}'.format(int(hours)), '{:0>2}'.format(int(minutes)))

	duration = property(_get_duration)

	def clean(self):
		pay_record = get_pay_record(self)
		self.pay = pay_record['pay']
		self.pay_memo = pay_record['pay_memo']


	def get_absolute_url(self):
		return reverse('home',kwargs={})

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
	#instance.shift = get_qgenda_shift('mwebb@spsradiology.com','12/11/2017')
	instance.shift = get_qgenda_shift(instance.get_email(),instance.work_start_time.date().strftime('%m/%d/%Y'))
pre_save.connect(rl_pre_save_receiver, sender=TimeLog)
