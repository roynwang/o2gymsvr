# coding=utf-8
from django.db import models
import datetime
from utils import smsutils
from django.shortcuts import get_object_or_404
import json
from order.models import *
from django.db.models import get_model
from django.core.cache import cache
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver


class ChargePricing(models.Model):
	id = models.AutoField(primary_key=True)
        gym = models.IntegerField()
        price = models.IntegerField()
        gift = models.IntegerField()


# Create your models here.
class Finance(models.Model):
	id = models.AutoField(primary_key=True)
        gym = models.IntegerField()
	date = models.DateField()
	brief = models.CharField(max_length=512)
	by = models.CharField(max_length=128)
	op = models.CharField(max_length=128)
        cate = models.CharField(max_length=128)
        amount = models.IntegerField()
        channel = models.CharField(max_length=128)
        memo = models.CharField(max_length=512, blank=True, default="")
	created = models.DateTimeField(auto_now=True)
	reimburse = models.BooleanField(default=False)

class Flow(models.Model):
	id = models.AutoField(primary_key=True)
        gym = models.IntegerField()
	date = models.DateField()
        phone_call = models.IntegerField(default=0)
        direct = models.IntegerField(default=0)
        groupon = models.IntegerField(default=0)
        by_customer = models.IntegerField(default=0)


class GroupCourse(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=32)
	brief = models.CharField(max_length=1024, blank=True)
	pic = models.CharField(max_length=1024, default="[]")
	intensity = models.IntegerField() 
        serial = models.CharField(max_length=128)
        step = models.CharField(max_length=128)
        gym = models.IntegerField() 


class GroupCourseInstance(models.Model):
	id = models.AutoField(primary_key=True)
        course = models.IntegerField(null=True,blank=True)
        budget = models.IntegerField(default=6)
        coach = models.CharField(max_length=32)
        gym = models.IntegerField() 
	date = models.DateField()
        hour = models.IntegerField(default=0)
        price = models.IntegerField(default=90)

@receiver(pre_delete, sender=GroupCourseInstance)
def clear_all_book(sender, **kwargs):
    instance = kwargs["instance"]
    books = GroupCourseInstanceBook.objects.filter(course=instance.id)
    for book in books:
        book.delete()


class GroupCourseInstanceBook(models.Model):
	id = models.AutoField(primary_key=True)
        customer = models.CharField(max_length=32)
        coach = models.CharField(max_length=32)
        course = models.IntegerField()
	date = models.DateField()
        gym = models.IntegerField() 
        price = models.IntegerField(default=0)
        groupcourse_price = models.IntegerField(default=0)
        
        def consume(self):
            pass

        def update_coach(self):
            if not self.coach:
                course = GroupCourseInstance.objects.get(id=self.course)
                self.coach = course.coach
                self.save()

@receiver(pre_delete, sender=GroupCourseInstanceBook)
def cancel_book(sender, **kwargs):
        book = kwargs["instance"]
        Balance = get_model("usr","Balance")
        balance =  Balance.objects.get(name=book.customer,gym=book.gym)
        balance.cancelconsume(book.price)
        balance.cancelconsume_groupcourse(book.groupcourse_price)


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

class SelfTrain(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=32)
	gym = models.IntegerField()
	hour = models.IntegerField()
        date = models.DateField()

	
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
        hide_customers = models.BooleanField(default=False)
	

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
                customlist += self.get_charge_customers()
		if self.shared_gyms != None and self.shared_gyms != '':
			for g in self.get_shared_with():
				customlist += g.get_customers()
                                customlist += g.get_charge_customers()
		customlist = list(set(customlist))
		return customlist
        def get_charge_customers(self):
                ret = list(BalanceOrder.objects.filter(gym=self.id,status="completed") \
                        .values_list("customer",flat=True))
                print ret
                return ret

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

        group_course = models.IntegerField(default = 0)
        price = models.IntegerField(default = 0)
        discount = models.IntegerField(default = 0)
        coursetype = models.CharField(max_length=32,default="time")

        action_required = models.CharField(max_length=128,blank=True,null=True,default="")

        user_confirmed = models.BooleanField(default=False)


	def __unicode__(self):
		return str(self.date) + str(self.hour)
        def user_confirm(self):
            self.user_confirmed = True
            self.save()

        def create_newcustomer_survey(self):
            if Survey.objects.filter(courseid = self.id).count() > 0:
                return False
            if self.custom.booked_time.count() == 3:
                survey = {"title":"新客户小调查",\
                        "questions":[\
                        {"question":"我能感觉到教练的鼓励"},\
                        {"question":"我能理解教练讲解的要领"},\
                        {"question":"我学会了新的运动知识和技能"}\
                        ]}
                return survey
            return False

        def is_first_course(self):
            if self.coursetype == "trial":
                return False
            else:
                count = Schedule.objects.filter(custom = self.custom, \
                        coursetype__in = ["normal", "charge"] ).count()
                if count == 1:
                    return True

            #if no eval
            '''
            ecount = BodyEval.objects.filter(custom = self.custom).count()
            if ecount == 0:
                return True
            '''
            return False

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
                self.custom.save_owner(self.coach)
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
		
        ''' OBSOLETE
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
        '''

        def create_threshold_msg(self):
            ThresholdMsg.try_create_msg_by_frequency(self,\
                    4, 30, 31798,"4次奖励")
            ThresholdMsg.try_create_msg_by_frequency(self,\
                    5, 30, 31798,"5次奖励")
            ThresholdMsg.try_create_msg_by_frequency(self,\
                    6, 30, 31798,"6次奖励")
            ThresholdMsg.try_create_msg_by_frequency(self,\
                    7, 30, 31798,"7次奖励")


@receiver(post_save, sender=BodyEval)
def clear_required_action(sender, instance,created):
    if not created or instance.group.startswith("6."):
        return
    User = get_model("usr","User")
    usr = get_object_or_404(User, id=instance.name)
    usr.booked_time.all().update(action_required="")
	

class BodyEval(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64)
	date = models.DateField(default=datetime.date.today)
	option = models.CharField(max_length=64)
	value = models.CharField(max_length=64)
	unit = models.CharField(max_length=64, blank=True)
	group = models.CharField(max_length=64)
	comments = models.CharField(max_length=1024,blank=True,default="", null=True)
	img = models.CharField(max_length=512,blank=True,default="", null=True)
	risks = models.CharField(max_length=1024,blank=True,default="", null=True)

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

class Todo(models.Model):
	id = models.AutoField(primary_key=True)
        done = models.BooleanField(default=False)
        content = models.CharField(max_length=1024, default="")
        gym = models.IntegerField(default=0)
        by = models.CharField(max_length=64, default="")
	schedule_date = models.DateField(default=datetime.date.today)


class ThresholdMsg(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64, db_index=True)
        templateid = models.IntegerField()
        status = models.CharField(max_length=64,default="pending")
	created = models.DateTimeField(default=datetime.datetime.now())
        date = models.DateField()
        desc = models.CharField(max_length=1024,default="")


        @staticmethod
        def try_create_msg_by_frequency(schedule, frequncy, deltadays, templateid, desc):
            #check wthether existed
            '''
            customer = schedule.custom
            startday = datetime.datetime.today().date() + datetime.timedelta(days= -deltadays)

            times = customer.booked_time.filter(date__gt=startday).count()
            if times != frequncy:
                return
            #create if not existed
            c = ThresholdMsg.objects.filter(name=customer.name,templateid=templateid).count()
            if c == 0:
                ThresholdMsg.objects.create(name=customer.name,templateid=templateid,desc=desc, date=schedule.date)

            gym = schedule.order.gym
            for coach in gym.coaches.all():
                if coach.role != 'admin':
                    continue
                message = Message.objects.create(name=schedule.coach.name, \
                        by=schedule.custom.name, \
                        content=schedule.custom.displayname +"触发了奖励", \
                        link="", \
                        dismiss_date=schedule.date)
            '''


        def send_msg(self):
            if self.desc == '4次奖励':
    	        return smsutils.sendSMS(self.name, self.templateid, ','.join(["30","4"]))
            if self.desc == '5次奖励':
    	        return smsutils.sendSMS(self.name, self.templateid, ','.join(["30","5"]))
            if self.desc == '6次奖励':
    	        return smsutils.sendSMS(self.name, self.templateid, ','.join(["30","6"]))
            if self.desc == '7次奖励':
    	        return smsutils.sendSMS(self.name, self.templateid, ','.join(["30","7"]))

class Survey(models.Model):
	id = models.AutoField(primary_key=True)
        courseid = models.IntegerField()
        score = models.IntegerField()
	date = models.DateField(default=datetime.date.today)
	coach = models.CharField(max_length=32)
	customer = models.CharField(max_length=32)
	question = models.CharField(max_length=512)
	course_type = models.CharField(max_length=32, default="pt")

class Homework(models.Model):
	id = models.AutoField(primary_key=True)
	created_date = models.DateField()
        completed_date = models.CharField(max_length=32,default="",blank=True)
	customer = models.CharField(max_length=32)
	coach = models.CharField(max_length=32)
	detail =  models.TextField(blank=True, default="[]")

        
	

