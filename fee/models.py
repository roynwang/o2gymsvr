from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class GymFee(models.Model):
	id = models.AutoField(primary_key=True)
	gym = models.IntegerField(unique=True, db_index=True)
	balance =  models.IntegerField(default=0)
	coaches = models.TextField(default="[]")
	coach_count = models.IntegerField(default=0)

class CoachSalarySetting(models.Model):
	id = models.AutoField(primary_key=True)
	coach = models.IntegerField()
	gymfee = models.ForeignKey(GymFee, related_name="coach_salary_setting")
	base_salary = models.FloatField(default=0)
	yanglao = models.FloatField(default=0)
	yiliao = models.FloatField(default=0)
	shiye = models.FloatField(default=0)
	gongjijin = models.FloatField(default=0)
	xiaoshou = models.FloatField(default=0)
	xuke = models.FloatField(default=0)
	shangke = models.FloatField(default=0)
	fixed_shangke = models.FloatField(default=0)
	group_person = models.FloatField(default=0)

