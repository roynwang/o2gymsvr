from django.db import models

# Create your models here.

class User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=32, db_index=True, unique=True)
	iscoach = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now=True)
	avatar = models.CharField(max_length=256)

	upped = models.ManyToManyField("weibo.Weibo", related_name="up_by")
	fwded = models.ManyToManyField("weibo.Weibo", related_name="fwd_by")
	commented = models.ManyToManyField("weibo.Weibo", related_name="comment_by")

	upped_person = models.ManyToManyField("self", related_name="up_by")
	upnum = models.IntegerField(default=0)

	recommand_p = models.IntegerField(blank=True, null=True)
	
	def __unicode__(self):
		return self.name

class TimeLine(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.ForeignKey(User, to_field="name", unique=True, related_name="timeline")
	feed = models.ManyToManyField('weibo.Weibo', related_name="feeder")
	followedby = models.ManyToManyField('TimeLine', related_name='follows')
	refresh = models.ManyToManyField('weibo.Weibo')

	def __unicode__(self):
		return self.name
