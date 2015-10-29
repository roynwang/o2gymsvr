from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime


# Create your models here.

class User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64, db_index=True, unique=True)
	displayname = models.CharField(max_length=128)
	iscoach = models.BooleanField(default=False)
	created = models.DateTimeField(default=datetime.now())
	avatar = models.CharField(max_length=256,default=settings.DEFAULT_AVATAR)

	upped = models.ManyToManyField("weibo.Weibo", related_name="up_by", null=True)
	fwded = models.ManyToManyField("weibo.Weibo", related_name="fwd_by", null=True)
	commented = models.ManyToManyField("weibo.Weibo", related_name="comment_by",null=True)

	upped_person = models.ManyToManyField("self", related_name="up_by",null=True)
	upnum = models.IntegerField(default=0)

	recommand_p = models.IntegerField(blank=True, null=True)

	#for coach
	tags = models.CharField(max_length=64, blank=True, default="")
	introduction = models.CharField(max_length=1024, blank=True, default="") 

	order_count = models.IntegerField(default=0)
	rate = models.IntegerField(default=0)
	course_count = models.BigIntegerField(default=0)
	
	sex = models.BooleanField(default=True)
	signature = models.CharField(max_length=64, blank=True)

	def __unicode__(self):
		return self.name

class TimeLine(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.OneToOneField(User, to_field="name", unique=True, related_name="timeline")
	feed = models.ManyToManyField('weibo.Weibo', related_name="feeder")
	followedby = models.ManyToManyField('TimeLine', related_name='follows')
	refresh = models.ManyToManyField('weibo.Weibo')

	def __unicode__(self):
		return self.name

class WorkingDays(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64, db_index=True, unique=True)
	weekrest = models.CharField(max_length=32, default="")
	excep_rest = models.CharField(max_length=1024, default="")
	excep_work = models.CharField(max_length=1024, default="")
	out_hours = models.CharField(max_length=64, default="")
	noon_hours = models.CharField(max_length=32, default="")

