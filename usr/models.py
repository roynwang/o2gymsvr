# coding=utf-8
from django.db import models
from django.conf import settings
from django.utils import timezone
#from datetime import datetime
from business.models import *


# Create your models here.

class User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64, db_index=True, unique=True)
	displayname = models.CharField(max_length=128)
	iscoach = models.BooleanField(default=False)
	created = models.DateTimeField(default=datetime.datetime.now())
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
	
	openid = models.CharField(max_length=32,unique=True,db_index=True, blank=True, default="")

	role = models.CharField(max_length=32, default="customer")
	corps = models.CharField(max_length=512, default="[]")

	age = models.IntegerField(blank=True, null=True)

	can_book = models.BooleanField(default=True)

	birthday = models.DateField(blank=True, null=True)

	flag = models.IntegerField(default=0)

	trial = models.IntegerField(blank=True, null=True)

	comments = models.CharField(max_length=64, blank=True)
	emergency_contact = models.CharField(max_length=64, blank=True)

        def trySendEvalNotification(self, schedule):
            #1 should after 30 day after last eval
            evals = BodyEval.objects.filter(name=self.name).order_by("-date")
            if evals.count() == 0:
                return
            last_eval = evals[0]
            delta = schedule.date - last_eval.date 
            if delta.days < 30:
                return
            #2 train times should >= 8 in last 30 days
            startday = schedule.date + datetime.timedelta(days=-30)
            times = self.booked_time.filter(date__gt=startday).count()
            if times < 8:
                return
            #3 send all in the gym
            order = self.booked_time.order_by("-date")[0].order
            gym = order.gym
            message = Message.objects.create(name=schedule.coach.name, \
                        by=self.name, \
                        content= self.displayname +"需要进行数据测量", \
                        link="", \
                        dismiss_date=schedule.date)

            for coach in gym.coaches.all():
                if coach.role != 'admin' or coach.name == schedule.coach.name:
                    continue
                message = Message.objects.create(name=coach.name, \
                        by=self.name, \
                        content= self.displayname +"需要进行数据测量", \
                        link="", \
                        dismiss_date=schedule.date)


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

class FeedBack(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64, db_index=True)
	feedback = models.CharField(max_length=1024, default="")
	created = models.DateTimeField(default=datetime.datetime.now())


class Message(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64, db_index=True)
        done = models.BooleanField(default=False)
        link = models.CharField(max_length=512, default="")
        content = models.CharField(max_length=1024, default="")
        by = models.CharField(max_length=64, default="")
	created = models.DateTimeField(default=datetime.datetime.now())
	dismiss_date = models.DateField(default=datetime.date.today)














