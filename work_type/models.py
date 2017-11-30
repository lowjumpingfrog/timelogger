from django.conf import settings
from django.db import models

from django.core.urlresolvers import reverse


class WorkCategory(models.Model):

	name 				= models.CharField(max_length=125)
	start_time			= models.TimeField(auto_now=False,auto_now_add=False)
	stop_time			= models.TimeField(auto_now=False,auto_now_add=False)
	points_per_hr		= models.DecimalField(max_digits=4, decimal_places=3, blank=False)
	daytime_rate_factor = models.DecimalField(max_digits=4, decimal_places=3, blank=False)
	rate 				= models.DecimalField(max_digits=6, decimal_places=2, blank=False)
	timestamp 			= models.DateTimeField(auto_now_add=True)
	updated 			= models.DateTimeField(auto_now=True)

	# order the query sets by current first
	class Meta:
		ordering = ['-updated', '-timestamp']

	def get_absolute_url(self):
		return reverse('work_categories:list',kwargs={'pk': self.pk})

	def __str__(self):
		return self.name

	@property
	def title(self):
		return self.name