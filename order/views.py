from django.shortcuts import render,get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView 
from order.serializers import *
from order.payprocess import *
from usr.models import *
from business.models import *
from django.http import HttpResponseNotFound
from rest_framework import status
import time
import datetime
from ipware.ip import get_ip
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
import json
import pytz
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Count


def create_pay(request, billid,channel):
	order = get_object_or_404(Order,billid=int(billid))
	ch = PayProcess.get_charge(billid,
			channel,
			order.amount*100,
			get_ip(request),
			order.product.introduction,
			order.product.introduction)
	return JsonResponse(ch,status=status.HTTP_201_CREATED)

def isFirstOrder(coach,customer):
	#coach = get_object_or_404(User,id = coach)
	#customer = get_object_or_404(User,id = customer)
	count = Order.objects.filter(coach=coach, custom = customer).exclude(status="unpaid").count()
	print count
	return count == 0

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
		

class OrderItemById(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = OrderDetailSerializer
	def get_object(self):
		role = "customer"
		usr = get_object_or_404(User, name=self.kwargs["name"])
		'''
		if usr.iscoach:
			return get_object_or_404(Order, coach=usr, id=int(self.kwargs["orderid"]))
		else:
		'''
		return get_object_or_404(Order, id=int(self.kwargs["orderid"]))
	def update(self, request, *args, **kwargs):
		ret = super(OrderItemById,self).update(request,args, kwargs)
		order = self.get_object()
		if "amount" in request.data:
			order.product.price = request.data["amount"]
			order.product.save()
		return ret


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
	customobj = get_object_or_404(User,id=customer)
	coachobj = get_object_or_404(User,id=coach)
	productobj = get_object_or_404(Product,id=product)
	isfirst = isFirstOrder(coachobj,customobj)
	return Order.objects.create(billid=str(billid), custom=customobj, coach=coachobj, product=productobj,
			amount=productobj.price, status="unpaid",isfirst=isfirst, gym=coachobj.gym.all()[0])
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
		isfirst = isFirstOrder(coach,customer)
		print "is first"
		print isfirst
		print coach.gym.all()[0]
		order = Order.objects.create(
				custom = customer,
				coach = coach,
				billid = billid,
				paidtime = timezone.now(),
				status = "paid",
				product = product,
				amount = price,
				gym = coach.gym.all()[0],
				channel = "offline",
				isfirst = isfirst)
		if "product_duration" in request.data:
			order.duration = request.data["product_duration"]
			order.save()
		serializer = OrderSerializer(order)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

class GymSoldRange(APIView):
	def get(self,request,gymid):
		end = datetime.date.today()
		start = end - datetime.timedelta(days=30)
		orders = Order.objects.filter(gym=get_object_or_404(Gym,id=gymid),paidtime__range=[start,end]) \
				.extra({'paidday': "date_format(date(CONVERT_TZ(`paidtime`,'+00:00','+08:00')),'%%Y%%m%%d')"}) \
				.values('paidday') \
				.annotate(sold_pirce=Sum('amount')) \
				.annotate(sold_count=Count('amount'))
		return Response(orders)
				

class GymSoldDay(APIView):
	def cal_course_income(self,query):
		price = 0
		for course in query:
			product = course.order.product
			#tmpprice = float(course.order.amount)/float(product.amount)
			tmpprice = course.order.amount/product.amount
			price += tmpprice
			print str(course.order.amount) + ":" + str(product.amount) + ": " + str(tmpprice)
		return price

	def sum_price_course(self,gymid,day):
		day_obj = datetime.datetime.strptime(day,"%Y%m%d")
		coaches = Gym.objects.get(id=gymid).coaches.values_list("id", flat=True)
		books = Schedule.objects.filter(date = day_obj,coach__in = coaches)
		#print books.query
		return (books.count(),self.cal_course_income(books))
		

	def get(self,request,gymid, day):
		utc = pytz.utc
		tz = pytz.timezone('Asia/Chongqing')
		start = datetime.datetime.strptime(day,"%Y%m%d")
		start = tz.localize(start)
		end = start + datetime.timedelta(days=1)
		print start
		print end
		orders = Order.objects.filter(gym=get_object_or_404(Gym,id=gymid),paidtime__range=[start,end])
		'''
		orders = Order.objects.filter(gym=get_object_or_404(Gym,id=gymid),\
				paidtime__year=start.year,\
				paidtime__month=start.month,\
				paidtime__day=start.day)
		'''
		sold_price = orders.aggregate(Sum("amount"))["amount__sum"]
		sold_count = orders.count()  
		course_count, course_price = self.sum_price_course(gymid, day)
		return Response({"sold_price": sold_price, "sold_count":sold_count,"course_price":course_price, "course_count": course_count})


class GymCustomers(generics.ListAPIView):
	pagination_class = None
	serializer_class = SimpleUserSerilaizer
	def get_queryset(self):
		gym = get_object_or_404(Gym, id=self.kwargs["gymid"])
		print "xxxxxxxxxxxx"
		coaches = gym.coaches.values_list("name",flat=True)
		orders = Order.objects.filter(gym=gym)
		print "xxxxxxxxxxxx"
		customers = orders.values_list("custom",flat=True).distinct()
		print customers
		return User.objects.filter(name__in = customers).distinct()

		

