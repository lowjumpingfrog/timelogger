from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from work_type.models import WorkCategory
from reasons.models import Reasons
from facilities.models import Facilities
from .utils import get_qgenda_shift
from time import strftime


User = settings.AUTH_USER_MODEL


# Create your models here.

class TimeLog(models.Model):
	user			= models.ForeignKey(User,on_delete=models.DO_NOTHING)
	reason			= models.ForeignKey(Reasons,on_delete=models.DO_NOTHING)
	facility		= models.ForeignKey(Facilities,on_delete=models.DO_NOTHING)
	work_start_time	= models.DateTimeField(auto_now=False, auto_now_add=False)
	work_end_time	= models.DateTimeField(auto_now=False, auto_now_add=False)
	comment 		= models.CharField(max_length=255, null=True,blank=True)
	shift 			= models.CharField(max_length=255, null=True,blank=True)
	reconciled		= models.BooleanField(default=False)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.user.username + ' - ' + self.work_start_time.strftime('%m/%d/%Y')
	
	def get_email(self):
		return self.user.email

	def get_absolute_url(self):
		return reverse('home',kwargs={})

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
	#instance.shift = get_qgenda_shift('mwebb@spsradiology.com','12/11/2017')
	instance.shift = get_qgenda_shift(instance.get_email(),instance.work_start_time.date().strftime('%m/%d/%Y'))
pre_save.connect(rl_pre_save_receiver, sender=TimeLog)

'''
def rl_post_save_receiver(sender, instance,created, *args, **kwargs):
	print('saved.')
	print(instance.timestamp)

post_save.connect(rl_post_save_receiver, sender=RestaurantLocation)
'''