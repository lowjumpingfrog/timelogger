from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.

class Facilities(models.Model):
	facility 		= models.CharField(max_length=255, null=False,blank=False)

	class Meta:
		verbose_name_plural = "Facilities"

	def __str__(self):
		return self.facility
	
	def get_absolute_url(self):
		return reverse('home',kwargs={})