from django.db import models

# Create your models here.
class CrawlShopCount(models.Model):
	id = models.AutoField(primary_key=True)
        date = models.DateField()
        keyword = models.CharField(max_length=128)
        count = models.IntegerField()

