from django.conf.urls import patterns, url
from business.views import *
'''
c: course
g: gym
b: book
s: schedule
r: read
'''
urlpatterns = patterns('',
		url(r'^api/c/$', CourseList.as_view()),
		url(r'^api/c/(?P<pk>[0-9]+)/$', CourseItem.as_view()),
		url(r'^api/g/$', GymList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/$', GymItem.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/incomplete/$', GymIncompleteList.as_view()),
		#url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/b/$',ScheduleBulkCreate.as_view()),
		#schedule item
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/b/(?P<date>[0-9]{8})/(?P<hour>[0-9]{1,2})/$',ScheduleItem.as_view()),
		#schedule day booked items
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/b/(?P<date>[0-9]{8})/$',ScheduleList.as_view()),
		#read week booked items
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/w/(?P<date>[0-9]{8})/$',ScheduleForRead.as_view()),
		#read availiable hours in day
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/d/(?P<date>[0-9]{8})/$',DayAvaiableTime.as_view()),

		#body eval
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/e/$',BodyEvalDateView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/e/(?P<date>[0-9]{8})/$',BodyEvalByDateView.as_view()),
		url(r'^api/e/$',AllEvalOptionsView.as_view()),

		#train
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/t/$',TrainDateView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/t/(?P<date>[0-9]{8})/$',TrainByDateView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/t/(?P<date>[0-9]{8})/(?P<schedule>[0-9]+)/$',TrainByScheduleView.as_view()),
		url(r'^api/a/$',NearByView.as_view()),
		url(r'^api/a/(?P<pk>[0-9]+)/$', GymMap.as_view()),
		)
