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
		url(r'^api/sw/$', SimpleWorkoutActionList.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]+)/sw/$', SimpleWorkoutActionListSmart.as_view()),
		url(r'^api/sw/(?P<pk>[0-9]+)/$', SimpleWorkoutItem.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]+)/workout/(?P<cate>[0-9]+)/$', WorkoutActionList.as_view()),
                url(r'^api/(?P<customer>[0-9]{11})/sw/(?P<workoutid>[0-9]+)/$', CustomerWorkoutValueItem.as_view()),
                url(r'^api/(?P<customer>[0-9]{11})/targets/$', CustomerTargetList.as_view()),
                url(r'^api/target/(?P<pk>[0-9]+)/$', CustomerTargetItem.as_view()),
                url(r'^api/g/(?P<gymid>[0-9]+)/kanban/$', KanbanTaskList.as_view()),
                url(r'^api/kanban/(?P<pk>[0-9]+)/$', KanbanTaskItem.as_view()),
		)
