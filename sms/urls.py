from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
		url(r'^api/lg/$',PwdLogin.as_view()),
		url(r'^api/gr/$',GymReg.as_view()),
        url(r'^api/sms/$', SMSGet.as_view()),
        url(r'^api/sms/(?P<number>[0-9]+)/$', SMSVerify.as_view()),
        url(r'^api/wx/token/$', Wechat.as_view()),
        url(r'^api/wx/signature/$', WechatSignature.as_view()),
		)
