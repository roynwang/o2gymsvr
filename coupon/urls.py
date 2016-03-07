from django.conf.urls import patterns, url
from .views import *


urlpatterns = patterns('',
		url(r'^api/g/(?P<pk>[0-9]+)/d/(?P<date>[0-9]{8})/free/$',FreeCourseListView.as_view()),
		url(r'^api/f/(?P<pk>[0-9]+)/$',FreeCourseItemView.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/c/(?P<customerid>[0-9]+)/coupon/$',CouponListView.as_view()),
		url(r'^api/cpn/(?P<pk>[0-9]+)/$',CouponItemView.as_view())
		)
