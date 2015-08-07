from django.db import models

# Create your models here.

class Course(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=32)
	brief = models.CharField(max_length=1024, blank=True)
	price = models.IntegerField()
	gym = models.ForeignKey("Gym", to_field="name", related_name="courses")
	coach = models.ManyToManyField("usr.User", related_name="teaching")
	student = models.ManyToManyField("usr.User", related_name="studying")

	recommand_p = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return self.title
	
class Gym(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=32, unique=True)
	introduction = models.CharField(max_length=1024)
	imgs = models.CharField(max_length=1024)
	coaches = models.ManyToManyField('usr.User', related_name="gym")

	recommand_p = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return self.name

