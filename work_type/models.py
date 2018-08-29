from django.conf import settings
from django.db import models
from django.urls import reverse
from constance import config

class WorkGroup(models.Model):

	group 				= models.CharField(max_length=125)
	timestamp 			= models.DateTimeField(auto_now_add=True)
	updated 			= models.DateTimeField(auto_now=True)

	# order the query sets by current first
	class Meta:
		ordering = ['-updated', '-timestamp']
		verbose_name_plural = "Groups"

	def get_absolute_url(self):
		return reverse('home',kwargs={})

	def __str__(self):
		return self.group

	@property
	def title(self):
		return self.group


class WorkCategory(models.Model):

	day_choices = (('wkd','Week Day'),('wkend','Week End'),('hol','Holiday'),('any','Any Day'))

	work_category 		= models.CharField(max_length=125)
	group				= models.ForeignKey(WorkGroup,on_delete=models.DO_NOTHING,verbose_name='Group')
	day_flag			= models.CharField(max_length=6,choices = day_choices,verbose_name='Day')
	start_time			= models.TimeField(auto_now=False,auto_now_add=False)
	stop_time			= models.TimeField(auto_now=False,auto_now_add=False)
	points_per_hr		= models.DecimalField(max_digits=6, decimal_places=3, blank=False)
	#daytime_rate_factor = models.DecimalField(max_digits=6, decimal_places=3, blank=False)
	#rate 				= models.DecimalField(max_digits=6, decimal_places=2, blank=False)
	timestamp 			= models.DateTimeField(auto_now_add=True)
	updated 			= models.DateTimeField(auto_now=True)

	# order the query sets by current first
	class Meta:
		ordering = ['-updated', '-timestamp']
		verbose_name_plural = "Categories"

	def _get_rate(self):
		return round(config.DAY_RATE*float(self.points_per_hr),2)

	rate = property(_get_rate)

	def get_absolute_url(self):
		return reverse('work_categories:list',kwargs={'pk': self.pk})

	def __str__(self):
		return self.work_category

	@property
	def title(self):
		return self.work_category
