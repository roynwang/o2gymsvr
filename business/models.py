from django.db import models

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

	def __unicode__(self):
		return self.name

class Schedule(models.Model):
	id = models.AutoField(primary_key=True)
	date = models.DateField()
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


	def __unicode__(self):
		return str(self.date) + str(self.hour)

class BodyEval(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64)
	date = models.DateField(auto_now=True)
	option = models.CharField(max_length=64)
	value = models.CharField(max_length=64)
	unit = models.CharField(max_length=64)
	group = models.CharField(max_length=64)

class BodyEvalOptions(models.Model):
	id = models.AutoField(primary_key=True)
	option = models.CharField(max_length=64)
	unit = models.CharField(max_length=64)
	group = models.CharField(max_length=64)


class Train(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64)
	date = models.DateField(auto_now=True)
	weight = models.CharField(max_length=64)
	repeattimes = models.CharField(max_length=64)
	groupid = models.IntegerField()
	action_name = models.CharField(max_length=64)
	action_order = models.IntegerField()
	units = models.CharField(max_length=32)
	course = models.ForeignKey('Schedule', related_name="record", null=True)
