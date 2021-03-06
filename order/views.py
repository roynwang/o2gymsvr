from django.shortcuts import render,get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView 
from order.serializers import *
from order.payprocess import *
from usr.models import *
from django.http import HttpResponseNotFound
from rest_framework import status
import time
from ipware.ip import get_ip
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
import json
from django.http import JsonResponse
from django.utils import timezone


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
		ret = None
		if role == "coach":
			ret = Order.objects.filter(coach = usr)
		else:
			ret = Order.objects.filter(custom = usr)

		cname = self.request.GET.get("coach")
		if cname:
			print "xxxxxxxxxxxxx"
			c = get_object_or_404(User, name = cname)
			print c
			ret = ret.filter(coach = c)
		return ret
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
		return usr.products.exclude(product_type=1)



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
	return Order.objects.create(billid=str(billid), custom=customobj, coach=coachobj, product=productobj,
			amount=productobj.price, status="unpaid")
def update_order(billid, status):
	order = Order.objects.get(billid=billid)
	order.status = status
	order.save()
def pay_order(billid):
	order = Order.objects.get(billid=billid)
	order.paidtime = datetime.now()
	order.save()

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@permission_classes((AllowAny,))
def pay_callback(request):
	j = json.loads(request.body)
	print j
	if j["type"] == "charge.succeeded":
		charge = j["data"]["object"]
		if charge["paid"] == True:
			print "update status ... ... ..."
			order_no = charge["order_no"]
			print order_no
			order = get_object_or_404(Order, billid=int(order_no))
			order.status = "paid"
			order.paidtime = datetime.now()
			order.channel = charge["channel"]
			coach = order.coach
			coach.order_count += 1
			if order.schedule_set.count() == order.product.amount:
				order.status = "inprogress"
			order.save()
			coach.save()
			print order.status
	return JsonResponse({'msg':'done'}, status=status.HTTP_200_OK)


class ManualOrder(APIView):
	def post(self,request,name):
		coach = get_object_or_404(User,name=name)
		print "coach"
		print coach.id
		#get/create customer
		phone = self.request.data["customer_phone"]
		displayname = self.request.data["customer_displayname"]
		if User.objects.filter(name=phone).exists():
			customer = User.objects.get(name=phone)
		else:
			customer = User.objects.create(name=phone,displayname=displayname,iscoach=False)
		print customer
		#create product
		introduction = self.request.data["product_introduction"]
		price = self.request.data["product_price"]
		amount = self.request.data["product_amount"]
		promotion = self.request.data["product_promotion"]
		product = Product.objects.create(coach=coach,
				introduction=introduction,
				price = price,
				amount = amount,
				promotion = promotion,
				product_type = 1)
		print "created product"
		print product.id

		#create order
		billid = getbillid(coach.id, customer.id)
		order = Order.objects.create(
				custom = customer,
				coach = coach,
				billid = billid,
				paidtime = timezone.now(),
				status = "paid",
				product = product,
				amount = price,
				channel = "offline")
		serializer = OrderSerializer(order)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
				




		

