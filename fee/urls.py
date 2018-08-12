from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
        url(r'^api/g/(?P<gymid>[0-9]+)/sync/$', GymSync.as_view()),
        url(r'^api/g/(?P<gymid>[0-9]+)/salary/$', CoachSalaryView.as_view()),
        url(r'^api/g/(?P<gymid>[0-9]+)/salarysetting/$', GymCoachSalarySettingView.as_view()),
        url(r'^api/g/(?P<gymid>[0-9]+)/salarysetting/(?P<pk>[0-9]+)/$', GymCoachSalarySettingItemView.as_view()),
        url(r'^api/g/(?P<gymid>[0-9]+)/salary/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', SalaryReceiptList.as_view()),
        url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/salary/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', SalaryReceiptItemView.as_view())
    )
