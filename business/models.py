# coding=utf-8
from django.db import models
import datetime
from utils import smsutils
import json

# Create your models here.

class Course(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=32)
	brief = models.CharField(max_length=1024, blank=True)
	price = models.IntegerField()
	pic = models.CharField(max_length=256)
	gym = models.ForeignKey("Gym", to_field="name", related_name="courses")
	coach = models.ManyToManyField("usr.User", related_name="teaching")
	student = models.ManyToManyField("usr.User", related_name="studying")

	recommand_p = models.IntegerField(blank=True, null=True)

	created = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.title
	
class Gym(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=32, unique=True)
	introduction = models.CharField(max_length=1024)
	imgs = models.CharField(max_length=1024)
	address = models.CharField(max_length=256)
	coaches = models.ManyToManyField('usr.User', related_name="gym")
	recommand_p = models.IntegerField(blank=True, null=True)
	location = models.CharField(max_length=32)
	phone = models.CharField(max_length=32)
	mapid = models.IntegerField()
	distance = models.IntegerField(default=0)
	sms_notification = models.BooleanField(default=True)
	shared_gyms = models.CharField(max_length=512,blank=True,default="[]")
	

	def __unicode__(self):
		return self.name

	def get_shared_with(self):
		if self.shared_gyms == None or self.shared_gyms == '':
			return None
		ret = []
		for i in json.loads(self.shared_gyms):
			ret.append(Gym.objects.get(id=i))
		return ret
	def get_customers(self):
		ret = list(self.orders.values_list("custom", flat=True))
		return ret
	def get_all_customers(self):
		customlist = self.get_customers()
		if self.shared_gyms != None and self.shared_gyms != '':
			for g in self.get_shared_with():
				customlist += g.get_customers()
		customlist = list(set(customlist))
		return customlist

        def get_admin(self):
            ret = []
            for c in self.coaches.all():
                if c.role == "admin" :
                    ret.append(c)
            return ret


class Schedule(models.Model):
	id = models.AutoField(primary_key=True)
	date = models.DateField(db_index=True)
	hour = models.IntegerField(max_length=2)
	comment = models.CharField(max_length=1024,default="",blank=True)
	feedback = models.CharField(max_length=1024,default="",blank=True)
	order = models.ForeignKey('order.Order',null=True)
	coach = models.ForeignKey('usr.User',related_name="sealed_time")
	custom = models.ForeignKey('usr.User',related_name="booked_time")

	created = models.DateTimeField(auto_now=True)
	deleted = models.BooleanField(default=False)
	done = models.BooleanField(default=False)

	rate = models.IntegerField(blank=True)

	detail =  models.TextField(blank=True, default="[]")


	def __unicode__(self):
		return str(self.date) + str(self.hour)
	def sendSms(self):
                
                if self.order is None:
                        return True
		if self.order.gym.id != 20:
			return smsutils.sendBookNotification(self)
		return True
	def doneBook(self):
		self.done = True
		self.coach.course_count += 1
		self.save()
		self.coach.save()
                if not self.order is None:
		        self.order.done()
	def getprice(self):
		o = self.order
		'''
		if o.subsidy != 0:
			return o.subsidy
		'''
                if self.order is None:
                    return 0
		p = self.order.product
		price  = p.price/p.amount
		return price
		
        def send_launch_notification(self):
            if not self.order is None and self.order.amount != 0 and self.order.subsidy != 0:
                #1 send to coach
                message = Message.objects.create(name=self.coach.name, \
                        by=self.custom.name, \
                        content= self.custom.displayname +"需要订餐", \
                        link="", \
                        dismiss_date=self.date)
                #2 send to admin
                for admin in self.coach.get_coach_gym().get_admin():
                    if admin.name == self.coach.name:
                        continue
                    message = Message.objects.create(name=admin.name, \
                        by=self.custom.name, \
                        content= self.custom.displayname +"需要订餐", \
                        link="", \
                        dismiss_date=self.date)
		

class BodyEval(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64)
	date = models.DateField(default=datetime.date.today)
	option = models.CharField(max_length=64)
	value = models.CharField(max_length=64)
	unit = models.CharField(max_length=64, blank=True)
	group = models.CharField(max_length=64)

class BodyEvalOptions(models.Model):
	id = models.AutoField(primary_key=True)
	option = models.CharField(max_length=64)
	unit = models.CharField(max_length=64)
	group = models.CharField(max_length=64)

class HealthQues(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64)
	date = models.DateField(auto_now=True)
	option = models.CharField(max_length=64)
        valuetype = models.CharField(max_length=64)
	value = models.TextField()
	group = models.CharField(max_length=64)

class HealthQuesOptions(models.Model):
	id = models.AutoField(primary_key=True)
	option = models.CharField(max_length=64)
        valuetype = models.CharField(max_length=64)
	group = models.CharField(max_length=64)


class Train(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64)
	date = models.DateField()
	weight = models.CharField(max_length=64, blank=True)
	repeattimes = models.CharField(max_length=64, blank=True)
	groupid = models.IntegerField()
	action_name = models.CharField(max_length=64)
	action_order = models.IntegerField()
	units = models.CharField(max_length=32)
	course = models.ForeignKey('Schedule', related_name="record", null=True)

class Message(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64, db_index=True)
        done = models.BooleanField(default=False)
        link = models.CharField(max_length=512, default="")
        content = models.CharField(max_length=1024, default="")
        by = models.CharField(max_length=64, default="")
	created = models.DateTimeField(default=datetime.datetime.now())
	dismiss_date = models.DateField(default=datetime.date.today)

