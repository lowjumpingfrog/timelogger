from django.conf import settings
from django.db import models
#from django.contrib.auth.models import Group
from work_type.models import WorkGroup
from django.urls import reverse

# Create your models here.

class Reasons(models.Model):
	reason 			= models.CharField(max_length=255, null=False,blank=False,verbose_name='Reason')
	billable		= models.BooleanField(default=False,verbose_name='Is Billable')
	group			= models.ForeignKey(WorkGroup,on_delete=models.DO_NOTHING,verbose_name='Group')
	max_time		= models.SmallIntegerField(default=12,verbose_name='Hour Time Limit')
	comment_needed	= models.BooleanField(default=False)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = "Reasons"

	def __str__(self):
		return self.reason

	def get_absolute_url(self):
		return reverse('home',kwargs={})
