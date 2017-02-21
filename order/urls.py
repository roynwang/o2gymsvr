from django.conf.urls import patterns, url
from order.views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/o/available/$',AvailableOrderItem.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/o/$',OrderList.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/b/(?P<billid>[0-9]+)/$',OrderItemByBillid.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/o/(?P<orderid>[0-9]+)/$',OrderItemById.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/p/$',ProductList.as_view()),
		url(r'^api/p/(?P<pk>[0-9]+)/$',ProductItem.as_view()),
		url(r'^api/pay/(?P<billid>[0-9]+)/(?P<channel>wx|alipay)/$',create_pay),
		url(r'^api/pay/callback/$',pay_callback),
		url(r'^api/pay/chargecallback/$',charge_callback),
		url(r'^api/g/(?P<pk>[0-9]+)/saledetail/$', GymSaleDetail.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/manualorder/$',ManualOrder.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/deadorder/$', DeadOrderList.as_view()),
		url(r'^api/g/(?P<gymid>[0-9]+)/sold/$',GymSoldRange.as_view()),
		url(r'^api/g/(?P<gymid>[0-9]+)/chart/$',GymChart.as_view()),
		url(r'^api/g/(?P<gymid>[0-9]+)/sold/(?P<day>[0-9]+)/$',GymSoldDay.as_view()),
		url(r'^api/g/(?P<gymid>[0-9]+)/customers/$',GymCustomers.as_view()),
		url(r'^api/g/(?P<gymid>[0-9]+)/customers/frequently/$',GymCustomersFreuently.as_view()),
		url(r'^api/g/(?P<gymid>[0-9]+)/trialcustomers/$',GymTrialCustomerList.as_view()),
		url(r'^pay/success/$',alipay_success),
		url(r'^pay/cancel/$',TemplateView.as_view(template_name="paycancel.html")),
		url(r'^api/g/(?P<gymid>[0-9]+)/backup/$',GymBackup.as_view()),
		)
