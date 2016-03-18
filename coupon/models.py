from django.db import models

# Create your models here.

class FreeCourse(models.Model):
	id = models.AutoField(primary_key=True)
	coach = models.IntegerField()
	customer = models.CharField(max_length=32,null=True, blank=True)
	day = models.DateField()
	hour = models.IntegerField()
	budget = models.IntegerField(default=1)
	sealed = models.IntegerField(default=0)
	gym = models.IntegerField()
	displayname = models.CharField(max_length=32,null=True, blank=True)
	sex = models.BooleanField(default=False)

	def hasSeat(self):
		return budget > sealed


class Coupon(models.Model):
	id = models.AutoField(primary_key=True)
	code = models.CharField(max_length=32)
	customer = models.IntegerField(null=True,blank=True)
	used = models.BooleanField(default=False)
	by = models.IntegerField()
	detail = models.TextField()
	valid_date = models.DateField()
	created = models.DateTimeField(auto_now_add=True)
	gym = models.IntegerField()
 	
