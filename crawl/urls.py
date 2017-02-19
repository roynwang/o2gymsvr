from django.conf.urls import patterns, url,include
from crawl.views import *

urlpatterns = patterns('',
        url(r'^api/cwl/shopcount/(?P<keyword>.+)/$', CrawlShopCountList.as_view()),
)
