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
	
