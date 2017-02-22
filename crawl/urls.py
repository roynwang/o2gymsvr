from django.conf.urls import patterns, url,include
from crawl.views import *

urlpatterns = patterns('',
        url(r'^api/cwl/shopcount/(?P<keyword>.+)/$', CrawlShopCountList.as_view()),
        url(r'^api/cwl/task/$', TaskList.as_view()),
        url(r'^api/cwl/task/latest/$', LatestTask.as_view()),
        url(r'^api/cwl/task/(?P<pk>[0-9]+)/$', TaskItem.as_view()),
)
