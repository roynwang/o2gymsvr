from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
        url(r'^api/g/(?P<gymid>[0-9]+)/sync/$', GymSync.as_view()),
        url(r'^api/g/(?P<gymid>[0-9]+)/salary/$', CoachSalaryView.as_view()),
        url(r'^api/g/(?P<gymid>[0-9]+)/salarysetting/$', GymCoachSalarySettingView.as_view()),
        url(r'^api/g/(?P<gymid>[0-9]+)/salarysetting/(?P<pk>[0-9]+)$', GymCoachSalarySettingItemView.as_view()),
		)
