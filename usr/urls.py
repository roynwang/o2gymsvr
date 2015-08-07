from django.conf.urls import patterns, url
from usr.views import *

urlpatterns = patterns('',
		url(r'^api/u/$', UserList.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/$', UserItem.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/timeline$', TimeLineItem.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/(?P<action>follow|unfollow)/$', Follow.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/feed/$', Feed.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/refresh/$', Refresh.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/album/$', Album.as_view()),
        url(r'^api/(?P<by>[a-zA-Z0-9]{4,20})/u/(?P<personname>[a-zA-Z0-9]{4,20})/(?P<upaction>up|down)/$', PersonUp.as_view()),
		)
