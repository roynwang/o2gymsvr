from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'o2gym.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^ios-notifications/', include('ios_notifications.urls')),
	url(r'^', include('traincategory.urls')),
    url(r'^', include('business.urls')),
    url(r'^', include('weibo.urls')),
    url(r'^', include('usr.urls')),
    url(r'^', include('order.urls')),
    url(r'^', include('recommend.urls')),
    url(r'^', include('sms.urls')),
]
