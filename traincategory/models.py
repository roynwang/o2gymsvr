from django.db import models
from django.shortcuts import render,get_object_or_404

# Create your models here.
class WorkoutCategeory(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=32)
	icon = models.CharField(max_length=256)
	def __unicode__(self):
		return self.name

class WorkoutAction(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=32)
	workouttype = models.CharField(max_length=32,blank=True,default="")
	muscle = models.CharField(max_length=32,blank=True, default="")
	categeory = models.ForeignKey(WorkoutCategeory, related_name="actions")
	units = models.CharField(max_length=32,blank=True, default="")
	by = models.CharField(max_length=64,blank=True, default="")
	

class SimpleWorkoutAction(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=32)
	unit = models.CharField(max_length=32,blank=True, default="")
        weight = models.IntegerField(default=10)
	repeattimes = models.IntegerField(default=4)
	comments = models.CharField(blank=True,max_length=128, default="")

class NewSimpleWorkoutAction(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=32)
	unit1 = models.CharField(max_length=32,blank=True, default="")
        value1 = models.IntegerField(default=10)
	unit2 = models.CharField(max_length=32,blank=True, default="")
        value2 = models.IntegerField(default=10)
	unit3 = models.CharField(max_length=32,blank=True, default="")
        value3 = models.IntegerField(default=10)


class CustomerWorkoutValue(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=32)
	customer = models.CharField(max_length=32)
	unit = models.CharField(max_length=32,blank=True, default="")
	weight = models.IntegerField()
	repeattimes = models.IntegerField(default=0)
	comments = models.CharField(max_length=128, default="")
	workoutid = models.IntegerField()

