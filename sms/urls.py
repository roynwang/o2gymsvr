from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
        url(r'^api/sms/$', SMSGet.as_view()),
        url(r'^api/sms/(?P<number>[0-9]+)/$', SMSVerify.as_view()),
		)
