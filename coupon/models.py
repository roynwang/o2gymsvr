from django.db import models
from usr.models import *
from utils import smsutils

# Create your models here.
TimeMap = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00"]


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
	coupon = models.CharField(max_length=256, null=True, blank=True)
	badge = models.CharField(max_length=256, null=True, blank=True)

	def hasSeat(self):
		return budget > sealed

	def sendCoachNoti(self):
		tplid=21767
		timestr = str(self.day)[5:] + " " + TimeMap[self.hour]
		coach = User.objects.get(id=self.coach)
		print smsutils.sendSMS(coach.name, tplid,",".join([self.displayname,str(self.customer),timestr]))
		print "coach noti sent"

	def sendCustomerNoti(self):
		tplid=17152
		coach = User.objects.get(id=self.coach)
		timestr = str(self.day)[5:] + " " + TimeMap[self.hour]
		print smsutils.sendSMS(self.customer, tplid,",".join([coach.displayname,timestr,coach.name,str(4)]))
		print "customer noti sent"


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
 	
		
