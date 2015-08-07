from django.db import models
import json

# Create your models here.
	
class Weibo(models.Model):
	id = models.AutoField(primary_key=True)

	title = models.CharField(max_length=16, blank = True)
	brief = models.CharField(max_length=128, blank = True)
	imgs = models.CharField(max_length=1024, blank = True)

	islong = models.BooleanField(default=False)

	created = models.DateTimeField(auto_now_add=True)

	by = models.ForeignKey("usr.User",to_field="name", related_name="history", on_delete=models.SET_NULL, null=True)

	iscomments = models.BooleanField(default=False)
	commentto = models.ForeignKey("weibo.Weibo", related_name="comments", null=True,
			on_delete=models.SET_NULL)

	isfwd = models.BooleanField(default=False)
	fwdfrom = models.ForeignKey("weibo.Weibo", null=True, on_delete=models.SET_NULL)

	upnum = models.IntegerField(default=0)
	commentnum = models.IntegerField(default=0)
	fwdnum = models.IntegerField(default=0)

	coach = models.ForeignKey("usr.User", related_name="student", null=True)

	recommand_p = models.IntegerField(blank=True, null=True)

	def top_comments(self):
		return self.comments.all()[:3]

	def __unicode__(self):
		weibo = {"id": self.id,
				"title": self.title,
				"brief": self.brief,
				"imgs": self.imgs,
				"created": str(self.created),
				"by": self.by.name,
				"islong": self.islong,
				}
		return json.dumps(weibo)
	class Meta:
		ordering = ['-created']


class LongWeibo(models.Model):
	id = models.AutoField(primary_key=True)
	weiboid = models.ForeignKey(Weibo, db_index=True)
	content = models.TextField()
	by = models.ForeignKey("usr.User", related_name="longweibolist", on_delete=models.SET_NULL,
			null=True)
	created = models.DateTimeField(auto_now=True)
	
class Images(models.Model):
	id = models.AutoField(primary_key=True)
	url = models.CharField(max_length=256)
	by = models.ForeignKey('usr.User', related_name="album")
	created = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.url
