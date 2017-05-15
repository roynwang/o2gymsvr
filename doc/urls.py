from django.conf.urls import patterns, url
from doc.views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
		url(r'^api/g/(?P<gymid>[0-9]+)/docs/$',GymDocList.as_view()),
		url(r'^api/g/(?P<gymid>[0-9]+)/video/$',GymVideoList.as_view()),
		)
