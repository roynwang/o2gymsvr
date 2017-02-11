from django.conf.urls import patterns, url
from .views import *
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = patterns('',
		url(r'^console/forget/$',TemplateView.as_view(template_name="console/forget.html")),
		url(r'^console/register/$',TemplateView.as_view(template_name="console/registration.html")),
		url(r'^console/login/$',auth_views.login, {'template_name': 'console/login.html'}),
		url(r'^console/dashboard/$', TemplateView.as_view(template_name="console/dashboard.html")),
		url(r'^whatsnew/$', TemplateView.as_view(template_name="console/whatsnew.html")),
		)
