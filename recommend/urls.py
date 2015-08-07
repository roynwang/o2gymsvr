from django.conf.urls import patterns, url
from recommend.views import *

urlpatterns = patterns('',
		url(r'^api/r/$', RecommendList.as_view()),
		url(r'^api/r/(?P<pk>[0-9]+)/$', RecommendItem.as_view()),
		url(r'^api/r/(?P<pk>[0-9]+)/(?P<rtype>person|gym|course|article)/(?P<itemid>[0-9]+)/$',
			RecommendAdd.as_view()),
		)
