from django.db import models
import datetime

# Create your models here.
class GymDoc(models.Model):
	id = models.AutoField(primary_key=True)
        gym = models.IntegerField()
        author = models.CharField(max_length=128)
        title = models.CharField(max_length=256)
        summary = models.CharField(max_length=256)
        attachment = models.CharField(max_length=256)
        datestr = models.CharField(max_length=64, default="")
        update = models.DateTimeField(default=datetime.datetime.now())


class GymVideo(models.Model):
	id = models.AutoField(primary_key=True)
        gym = models.IntegerField()
        pic = models.CharField(max_length=256)
        uploader = models.CharField(max_length=128)
        coach = models.CharField(max_length=128)
        title = models.CharField(max_length=256)
        summary = models.CharField(max_length=1024)
        attachment = models.CharField(max_length=256)
        update = models.DateTimeField(default=datetime.datetime.now())
        datestr = models.CharField(max_length=64, default="")

        '''    
        def update_keyword(self):
            words = self.keywords.split(" ")
            queryset = GymVideo.objects.filter(gym=self.gym,videoid=self.id)
            for row in queryset:
                if not row.keyword in  words:
                    row.remove()
                else:
                    words.remove(row.keyword)
            for word in words:
                GymVideo.objects.create(gym=self.gym,videoid=self.id,keyword = word)
        '''
                            


class GymVideoKeyword(models.Model):
	id = models.AutoField(primary_key=True)
        gym = models.IntegerField()
        keyword = models.CharField(max_length=128)
        videoid = models.IntegerField()
        

