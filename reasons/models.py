from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group
from django.urls import reverse

# Create your models here.

class Reasons(models.Model):
	reason 			= models.CharField(max_length=255, null=False,blank=False)
	group 			= models.ForeignKey(Group,on_delete=models.DO_NOTHING)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = "Reasons"

	def __str__(self):
		return self.reason + ' - ' + str(self.group)
	
	def get_absolute_url(self):
		return reverse('home',kwargs={})