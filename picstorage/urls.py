from django.conf.urls import patterns, url
from picstorage.views import *

urlpatterns = patterns('',
		url(r'^api/u/$', UserList.as_view()),
		)
