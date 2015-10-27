from django.conf.urls import patterns, url
from .views import *
'''
c: course
g: gym
b: book
s: schedule
r: read
'''
urlpatterns = patterns('',
		url(r'^api/w/$', WorkoutCategeoryList.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]+)/workout/(?P<cate>[0-9]+)/$', WorkoutActionList.as_view())
		)
