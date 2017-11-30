from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from work_type.models import WorkCategory


User = settings.AUTH_USER_MODEL


# Create your models here.

class TimeLog(models.Model):
	user			= models.ForeignKey(User) # Django Models Unleashed JOINCFE.com
	category		= models.ForeignKey(WorkCategory)
	work_start_time	= models.DateTimeField(auto_now=False, auto_now_add=False)
	work_end_time	= models.DateTimeField(auto_now=False, auto_now_add=False)
	comment 		= models.CharField(max_length=255, null=True,blank=True)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.user.username + ' - ' + self.work_start_time.strftime('%m/%d/%Y')
	
	def get_absolute_url(self):
		#return f"/restaurants/{self.slug}"
		return reverse('home',kwargs={})