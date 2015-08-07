from django.db import models

# Create your models here.
RECOMMENDTYPE= (('article','article'), ('user','user'), ('gym','gym'),('course','course'))
CORNERCHOICE = (('recommend','recommend'),('hot','hot'))

class Recommend(models.Model):
	id = models.AutoField(primary_key=True)
	created = models.DateTimeField(auto_now=True)
	recommend_type = models.CharField(max_length=16, choices=RECOMMENDTYPE)
	article = models.ForeignKey('weibo.Weibo', null=True)
	person = models.ForeignKey('usr.User', null=True)
	gyms = models.ForeignKey('business.Gym', null=True)
	course = models.ForeignKey('business.Course', null=True)
	recommend_title = models.CharField(max_length=64)
	recommend_pic = models.CharField(max_length=512)
	recommend_subtitle = models.CharField(max_length=512, blank=True)
	recommend_loc = models.CharField(max_length=64,blank=True)
	recommend_price = models.CharField(max_length=64,blank=True)
	corner = models.CharField(max_length=12, choices=CORNERCHOICE, blank=True)
