from django.conf.urls import patterns, url
from weibo.views import *

urlpatterns = patterns('',
        #url(r'^api/weibo/$', WeiboListAll.as_view()),
        url(r'^api/w/(?P<pk>[0-9]+)/$', WeiboItem.as_view()),
        url(r'^api/(?P<by>[a-zA-Z0-9]{4,20})/weibo/$', WeiboList.as_view()),
        url(r'^api/(?P<by>[a-zA-Z0-9]{4,20})/w/(?P<weiboid>[0-9]+)/comment/$', CommentList.as_view()),
        url(r'^api/(?P<by>[a-zA-Z0-9]{4,20})/w/(?P<weiboid>[0-9]+)/(?P<upaction>up|down)/$', WeiboUp.as_view()),

        url(r'^api/(?P<by>[a-zA-Z0-9]{4,20})/l/(?P<weiboid>[0-9]+)/$', LongWeiboItem.as_view(), name='longweibo-detail'),
        url(r'^api/(?P<by>[0-9]+)/i/(?P<pk>[0-9]+)/$', ImageItem.as_view()),
        url(r'^api/l/$', LongWeiboList.as_view()),
		url(r'^api/p/token/$', PicToken.as_view()),
		url(r'^api/l/(?P<weiboid>[0-9]+)/$', ArticlePage.as_view()),
		)
