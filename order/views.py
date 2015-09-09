from django.shortcuts import render,get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from order.serializers import *
from order.payprocess import *
from usr.models import *
from django.http import HttpResponseNotFound
from rest_framework import status
import time
from ipware.ip import get_ip
from django.http import JsonResponse


def create_pay(request, billid,channel):
	order = get_object_or_404(Order,billid=int(billid))
	ch = PayProcess.get_charge(billid,
			channel,
			order.amount*100,
			get_ip(request),
			order.product.introduction,
			order.product.introduction)
	return JsonResponse(ch,status=status.HTTP_201_CREATED)
	

class OrderList(generics.ListCreateAPIView):
	serializer_class = OrderSerializer
	def get_queryset(self):
		#role =  self.request.query_params.get('role', None)
		usr = get_object_or_404(User, name=self.kwargs["name"])
		print usr
		role = 'usr'
		if usr.iscoach:
			role = "coach"
		#testc = get_object_or_404(User, name="alex")
		#create_order(usr,testc)
		if role == "coach":
			return Order.objects.filter(coach = usr)
		else:
			return Order.objects.filter(custom = usr)
	def create(self,request, *args, **kwargs):
		print request.data
		obj = create_order(request.data["custom"],request.data["coach"], request.data["product"])
		return Response(OrderSerializer(instance=obj).data, status=status.HTTP_201_CREATED) 
		

class OrderItemById(generics.RetrieveUpdateAPIView):
	serializer_class = OrderDetailSerializer
	def get_object(self):
		role = "customer"
		usr = get_object_or_404(User, name=self.kwargs["name"])
		if usr.iscoach:
			return get_object_or_404(Order, coach=usr, id=int(self.kwargs["orderid"]))
		else:
			return get_object_or_404(Order, custom=usr, id=int(self.kwargs["orderid"]))


class OrderItemByBillid(generics.RetrieveAPIView):
	serializer_class = OrderDetailSerializer
	def get_object(self):
		role = "customer"
		usr = get_object_or_404(User, name=self.kwargs["name"])
		if usr.iscoach:
			return get_object_or_404(Order, coach=usr, billid=int(self.kwargs["billid"]))
		else:
			return get_object_or_404(Order, custom=usr, billid=int(self.kwargs["billid"]))

class ProductList(generics.ListCreateAPIView):
	serializer_class = ProductSerializer
	pagination_class = None
	def get_queryset(self):
		usr = get_object_or_404(User, name=self.kwargs["name"])
		return Product.objects.filter(coach=usr)

class ProductItem(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = ProductSerializer
	queryset = Product.objects.all()

def getbillid(customerid, coachid):
	ts = int(time.time())
	return int(str(ts) + str(customerid) + str(coachid))
	
def create_order(customer, coach, product):
	billid = getbillid(customer, coach)
	print "xxxxxxxxxxxxxx"
	customobj = get_object_or_404(User,id=customer)
	coachobj = get_object_or_404(User,id=coach)
	productobj = get_object_or_404(Product,id=product)
	print "xxxxxxxxxxxxxx"
	return Order.objects.create(billid=billid, custom=customobj, coach=coachobj, product=productobj,
			amount=productobj.price, status="unpaid")
def update_order(billid, status):
	order = Order.objects.get(billid=billid)
	order.status = status
	order.save()
def pay_order(billid):
	order = Order.objects.get(billid=billid)
	order.paidtime = datetime.now()
	order.save()

