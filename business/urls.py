from django.conf.urls import patterns, url
from business.views import *

urlpatterns = patterns('',
		url(r'^api/c/$', CourseList.as_view()),
		url(r'^api/c/(?P<pk>[0-9]+)/$', CourseItem.as_view()),
		url(r'^api/g/$', GymList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/$', GymItem.as_view()),
		)
