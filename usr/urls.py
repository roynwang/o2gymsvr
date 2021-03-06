from django.conf.urls import patterns, url,include
from usr.views import *

urlpatterns = patterns('',
		url(r'^api/n/',register),
		url(r'^api/v/$','rest_framework_jwt.views.obtain_jwt_token'),
		url(r'^api/t/', 'rest_framework_jwt.views.refresh_jwt_token'),
		url(r'^api/u/$', UserList.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/$', UserItem.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/timeline$', TimeLineItem.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/(?P<action>follow|unfollow)/$', Follow.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/feed/$', Feed.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/refresh/$', Refresh.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/album/$', Album.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/courses/$', Courses.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/comments/$', CoachComments.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/customers/$', CustomerList.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/rest/$', WorkingDaysView.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/gym/$', ModifyGym.as_view()),
        url(r'^api/(?P<by>[a-zA-Z0-9]{4,20})/u/(?P<personname>[a-zA-Z0-9]{4,20})/(?P<upaction>up|down)/$', PersonUp.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/income/$', InCome.as_view()),
		)
