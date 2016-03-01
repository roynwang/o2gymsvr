from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
		# Examples:
		# url(r'^$', 'o2gym.views.home', name='home'),
		# url(r'^blog/', include('blog.urls')),
	#	url(r'^favicon.ico$','django.views.generic.simple.redirect_to',{'url':'/static/images/favicon.ico'}),
		url(r'^$',TemplateView.as_view(template_name="index.html")),
		url(r'^',include("console.urls")),
		url(r'^api/protocol/$',TemplateView.as_view(template_name="agreement.html")),
		url(r'^admin/', include(admin.site.urls)),
		url(r'^', include('traincategory.urls')),
		url(r'^', include('business.urls')),
		url(r'^', include('weibo.urls')),
		url(r'^', include('usr.urls')),
		url(r'^', include('order.urls')),
		url(r'^', include('recommend.urls')),
		url(r'^', include('sms.urls')),
		url(r'^', include('fee.urls')),
		url(r'^mobile/home/$', TemplateView.as_view(template_name="mobile/home.html")),
		url(r'^mobile/login/$', TemplateView.as_view(template_name="mobile/login.html")),
		url(r'^mobile/i/$', TemplateView.as_view(template_name="customermobile/home.html")),
		url(r'^gym/home/$', TemplateView.as_view(template_name="storesale.html")),
		]
