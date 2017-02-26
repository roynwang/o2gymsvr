from django.db import models
from crawl.crawlhandler import *

# Create your models here.
class CrawlShopCount(models.Model):
	id = models.AutoField(primary_key=True)
        date = models.DateField()
        keyword = models.CharField(max_length=128)
        count = models.IntegerField()


class CrawlGrouponCount(models.Model):
	id = models.AutoField(primary_key=True)
        date = models.DateField()
        keyword = models.CharField(max_length=128)
	shopid = models.IntegerField()
	grouponid = models.IntegerField()
        shopname = models.CharField(max_length=512)
        grouponname = models.CharField(max_length=512)
	price = models.IntegerField()
        sold_until_now = models.IntegerField()
        sold = models.IntegerField()



class CrawlTask(models.Model):
	id = models.AutoField(primary_key=True)
        date = models.DateField()
        city = models.CharField(max_length=32,default="beijing")
        keyword = models.CharField(max_length=128)
        url = models.CharField(max_length=1024,default="")
        status = models.CharField(max_length=32, default="init") #inited crawling 
        handler = models.CharField(max_length=32, default="list")
        html = models.TextField(default="")
	created = models.DateTimeField(auto_now_add=True)


        def handle_list(self):
            handler = ListHandler(self)
            groupons = handler.get_groupon_list()
            for groupon in groupons:
                #insert into groupon table
                sold = 0
                #if existed
                if CrawlGrouponCount.objects.filter(grouponid=groupon['grouponid'],date=self.date).count() != 0:
                    continue

                #cacluate the sold count between the duration
                if CrawlGrouponCount.objects.filter(grouponid=groupon['grouponid']).count() != 0:
                    tmp =CrawlGrouponCount.objects.filter(grouponid=groupon['grouponid'])\
                            .order_by("-date")[0]
                    sold = groupon['sold_until_now'] - tmp.sold_until_now

                CrawlGrouponCount.objects.create(\
                            date=self.date,\
                            keyword=self.keyword,\
                            shopid = groupon['shopid'],\
                            grouponid = groupon['grouponid'],\
                            shopname = groupon['shopname'],\
                            grouponname = groupon['grouponname'],\
                            price = groupon['price'],\
                            sold_until_now = groupon['sold_until_now'],\
                            sold = sold)

            #skip creating sub tasks if not the first page
            if len(groupons) == 40:
                pagenum = handler.get_current_page_num()
                newpage = pagenum
                q = self.keyword.replace(" ","+")
                url = "http://t.dianping.com/list/"+self.city+"?q="+ q + "&pageIndex=" + str(newpage)
                CrawlTask.objects.get_or_create(\
                        date=self.date,\
                        keyword=self.keyword,\
                        url=url)

            '''
            if not handler.is_first_page():
                return
            for url in handler.extract_page_url():
                CrawlTask.objects.create(\
                        date=self.date,\
                        keyword=self.keyword,\
                        url=url)
            '''
                

        



