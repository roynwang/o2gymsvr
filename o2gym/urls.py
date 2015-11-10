from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
		# Examples:
		# url(r'^$', 'o2gym.views.home', name='home'),
		# url(r'^blog/', include('blog.urls')),
	#	url(r'^favicon.ico$','django.views.generic.simple.redirect_to',{'url':'/static/images/favicon.ico'}),
		url(r'^$',TemplateView.as_view(template_name="index.html")),
		url(r'^console/login$',TemplateView.as_view(template_name="console/login.html")),
		url(r'^api/protocol/$',TemplateView.as_view(template_name="agreement.html")),
		url(r'^admin/', include(admin.site.urls)),
		url(r'^', include('traincategory.urls')),
		url(r'^', include('business.urls')),
		url(r'^', include('weibo.urls')),
		url(r'^', include('usr.urls')),
		url(r'^', include('order.urls')),
		url(r'^', include('recommend.urls')),
		url(r'^', include('sms.urls')),
		]
