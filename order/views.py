# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
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
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
import json
import pytz
import pprint
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Count
from random import randint
from utils import smsutils
from utils import wxutils 
from django.conf import settings
from sms.models import *
import os
from django.http import Http404
import xmltodict


def create_pay(request, order,channel):
	#order = get_object_or_404(Order,billid=int(billid))
	ch = PayProcess.get_charge(order.billid,
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
			ret = Order.objects.filter(coach = usr).exclude(paidtime = None)
		else:
			ret = Order.objects.filter(custom = usr)

		cname = self.request.GET.get("coach")
		if cname:
			c = get_object_or_404(User, name = cname)
			ret = ret.filter(coach = c)
		return ret
	def create(self,request, *args, **kwargs):
		print request.data
		obj = create_order(request.data["custom"],request.data["coach"], request.data["product"])
		return Response(OrderSerializer(instance=obj).data, status=status.HTTP_201_CREATED) 


class AvailableOrderItem(generics.RetrieveAPIView):
	serializer_class = OrderSerializer
	def get_object(self):
                #get
		usr = get_object_or_404(User, name=self.kwargs["name"])
                #gymid = self.request.data['gym']
                #ret = usr.orders.exclude(gym=get_object_or_404(Gym,id=gymid), status__in=["unpaid","done"]).order_by('paidtime')[:1]
                ret = usr.orders.exclude(status__in=["unpaid","done"]).order_by('paidtime')
            
                for item in ret:
                    item.done()
                    return item
                raise Http404


class ChargeScheduleList(generics.ListAPIView):
	serializer_class = ScheduleSimpleSerializer
        pagination_class = None
        def get_queryset(self):
	    usr = get_object_or_404(User, name=self.kwargs["name"])
            return Schedule.objects.filter(order=None,coursetype="charge",custom=usr).order_by("-date")

        

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
		'''
		if "coach" in request. data:
			order.product.coach = get_object_or_404(User, id=request.data["coach"])
			order.product.save()
		'''
		return ret
	def delete(self, request, *args, **kwargs):
            order = self.get_object()
            Schedule.objects.filter(order=order).delete()
	    return super(OrderItemById,self).delete(request,args, kwargs)
            



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
	order.paidtime = datetime.datetime.now()
	order.save()

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@permission_classes((AllowAny,))
def charge_callback(request):
    #TODO load xml
    result = "SUCCESS"
    req = xmltodict.parse(request.body)
    req  = req['xml']
    if req['result_code'] != "SUCCESS":
        result = "FAIL"
    else:
        billid = req['out_trade_no']
        balance_order = BalanceOrder.objects.get(billid=billid)
        b,_ = Balance.objects.get_or_create(name=balance_order.customer,gym=balance_order.gym)
        pprint.pprint(b)
        b.complete_order(balance_order)
    body = "<xml><return_code><![CDATA["+result+"]]></return_code></xml>"
    return HttpResponse(body, content_type='text/xml')
    

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
			order.paidtime = datetime.datetime.now()
			order.channel = charge["channel"]
			coach = order.coach
			coach.order_count += 1
			if order.schedule_set.count() == order.product.amount:
				order.status = "inprogress"
			order.save()
			coach.save()
			print order.status
	return JsonResponse({'msg':'done'}, status=status.HTTP_200_OK)

class GymChargeOrder(generics.ListAPIView):
	serializer_class = BalanceOrderSerializer
	pagination_class = None
	def get_queryset(self):
		start = datetime.datetime.strptime(self.request.GET["start"],"%Y%m%d") + datetime.timedelta(hours=8)
		end = datetime.datetime.strptime(self.request.GET["end"],"%Y%m%d") + datetime.timedelta(days=1) + datetime.timedelta(hours=8)
                return BalanceOrder.objects.filter(gym=self.kwargs.get("pk"),status="completed",updated__range=[start,end]).order_by("-updated")


class ChargeOrder(APIView):
	def post(self,request,name):
		#get/create customer
                customer = get_object_or_404(User,name=name)
                priceitem = ChargePricing.objects.get(id=request.data['id'])
                gym = int(request.data['gym'])
                openid = wxutils.get_openid(request.data['code'])
                #openid = "obzf70EAA4fBncDhQwe9z24l19es"
		billid = getbillid(customer.id, 0)
                balance = BalanceOrder.objects.create(billid=billid,\
                        customer=name,\
                        gym=gym,\
                        amount=priceitem.price+priceitem.gift,\
                        paid_amount=priceitem.price,\
                        status="unpaid")
                #create wx pay
                title = "氧气训练馆-充值" + str(priceitem.price+priceitem.gift) + "元"
                charge = wxutils.create_charge(billid,openid,title,priceitem.price,get_ip(request))
                pprint.pprint(charge)
                resp = {
                        "appId":charge['xml']['appid'],\
                        "timeStamp": str(int(time.time())),\
                        "nonceStr": wxutils.GetRandomStr(),\
                        "package": "prepay_id="+charge['xml']['prepay_id'],\
                        "signType": "MD5"}
                resp['paySign'] = wxutils.getSign(resp)
                del resp["appId"]
	        return JsonResponse(resp, status=status.HTTP_200_OK)
                
            


class ManualOrder(APIView):
        def create_charge_order(self, request,name):
	    coach = get_object_or_404(User,name=name)
	    phone = self.request.data["customer_phone"]
	    displayname = self.request.data["customer_displayname"]
            #1.create user
	    if User.objects.filter(name=phone).exists():
		customer = User.objects.get(name=phone)
                customer.trial = None
                customer.save()
            else:
		sex = False
		if request.data["sex"] == '1':
		    sex = True
		customer = User.objects.create(name=phone,displayname=displayname,sex=sex,iscoach=False,created=datetime.datetime.now())
	    if "birthday" in self.request.data:
		customer.birthday = datetime.datetime.strptime(self.request.data["birthday"],"%Y-%m-%d").date()
		#customer.save()
	    if "emergency_contact" in self.request.data and self.request.data["emergency_contact"] != "":
		customer.emergency_contact = self.request.data["emergency_contact"]
		#customer.save()
	    customer.save()

            #2.create chage
            
            print("xxxxxxxxxxxxxxxxxxxxxxxx")
	    billid = getbillid(coach.id, customer.id)
	    gym = Gym.objects.get(name=coach.gym.all()[0])
            amount = int(request.data["product_promotion"]) + int(request.data["product_price"])
            paid = int(request.data["product_price"])

            balance_order = BalanceOrder.objects.create(billid = billid,\
                    customer = customer.name,\
		    amount = amount,\
		    paid_amount = paid,\
                    gym = gym.id,\
                    status="unpaid")
            b,_ = Balance.objects.get_or_create(name=balance_order.customer,gym=balance_order.gym)
            b.complete_order(balance_order)
	    serializer = BalanceOrderSerializer(balance_order)
	    return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            #create charge order

	def post(self,request,name):
                if request.data['ordertype'] == "charge":
                    return self.create_charge_order(request,name)

		coach = get_object_or_404(User,name=name)
		#get/create customer
		phone = self.request.data["customer_phone"]
		displayname = self.request.data["customer_displayname"]
		if User.objects.filter(name=phone).exists():
			customer = User.objects.get(name=phone)
                        customer.trial = None
                        customer.save()
		else:
			sex = False
			if request.data["sex"] == '1':
				sex = True
			customer = User.objects.create(name=phone,displayname=displayname,sex=sex,iscoach=False)

			if "advance" in request.data:
				print "##############sending register sms##############"
				#create user for customer 
				pwd = randint(100000,999999)
				auth_usr = get_user_model().objects.create_user(username=phone)
				auth_usr.set_password(pwd)
				auth_usr.save()
				num, _ =  Sms.objects.get_or_create(number=phone)
				num.vcode = pwd
				num.save()
				resp = smsutils.templateSMS(settings.UCPAASSID,
					settings.UCPAASTOKEN,
					settings.UCPAASAPPID,
					phone,
					settings.UCPAASTEMPLATE_REGISTER,
					str(pwd))
			

		if "age" in self.request.data:
			customer.age = self.request.data["age"]
			customer.save()
		if "birthday" in self.request.data:
			customer.birthday = datetime.datetime.strptime(self.request.data["birthday"],"%Y-%m-%d").date()
			customer.save()

		if "emergency_contact" in self.request.data and self.request.data["emergency_contact"] != "":
			customer.emergency_contact = self.request.data["emergency_contact"]
			customer.save()
		#create product
		introduction = self.request.data["product_introduction"]
		price = int(self.request.data["product_price"])
		amount = self.request.data["product_amount"]
		promotion = self.request.data["product_promotion"]
		subsidy = self.request.data["subsidy"]
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
				isfirst = isfirst,
				subsidy = subsidy)
		if "product_duration" in request.data:
			order.duration = int(request.data["product_duration"])
			order.save()

		#if "qr"
		if "channel" in request.data and request.data["channel"] != "offline":
			return self.trackQRPay(order, request, request.data["channel"])

		#if just create
		serializer = OrderSerializer(order)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	def trackQRPay(self, order, request, channel="alipay_qr"):
		#set to unpaid
		order.paidtime = None
		order.status = "unpaid"
		order.save()
		#create charge
		# alipay_qr
		return create_pay(request,order, channel)





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

class GymChart(APIView):
	def get(self,request,gymid):
		if "end" in request.GET:
			end = datetime.datetime.strptime(request.GET["end"], "%Y%m%d")
		else:
			end = datetime.date.today()

		if "start" in request.GET:
			start = datetime.datetime.strptime(request.GET["start"], "%Y%m%d")
		else:
		        start = end - datetime.timedelta(days=365)

		end = end + datetime.timedelta(days=1)

		orders = Order.objects.filter(gym=get_object_or_404(Gym,id=gymid),paidtime__range=[start,end]) \
				.extra({'paidday': "date_format(date(CONVERT_TZ(`paidtime`,'+00:00','+08:00')),'%%Y%%m')"}) \
				.values('paidday') \
				.annotate(sold_pirce=Sum('amount')) \
				.annotate(sold_count=Count('amount')) \
				.annotate(sold_course=Sum('product__amount'))
		return Response(orders)

class GymScheduleChart(APIView):
	def get(self,request,gymid):
		if "end" in request.GET:
			end = datetime.datetime.strptime(request.GET["end"], "%Y%m%d")
		else:
			end = datetime.date.today()

		if "start" in request.GET:
			start = datetime.datetime.strptime(request.GET["start"], "%Y%m%d")
		else:
		        start = end - datetime.timedelta(days=365)

		end = end + datetime.timedelta(days=1)
                schedules = Schedule.objects.filter(date__range=[start,end], done=True)
                ret = {"<30":0, "30-60":0,">60":0}
                for s in schedules:
                    if s.order is None or s.order.gym.id != 19:
                        continue
                    delta =  s.date - s.order.paidtime.date()
                    if delta.days <30:
                        ret['<30'] +=1;
                    if delta.days >=30 and delta.days<=60:
                        ret['30-60'] +=1;
                    if delta.days >60:
                        ret['>60'] +=1;
                return Response(ret)



class GymSoldDay(APIView):
	def cal_course_income(self,query):
		price = 0
		for course in query:
                        if course.order is None:
                                continue
			product = course.order.product
			#tmpprice = float(course.order.amount)/float(product.amount)
			tmpprice = course.order.amount/product.amount
			price += tmpprice
			print str(course.order.amount) + ":" + str(product.amount) + ": " + str(tmpprice)
		return price

        def cal_exp_course_count(self, query):
                c = 0
		for course in query:
                        if course.order is None:
                                c += 1
		return c
                

	def sum_price_course(self,gymid,day):
		day_obj = datetime.datetime.strptime(day,"%Y%m%d")
		coaches = Gym.objects.get(id=gymid).coaches.values_list("id", flat=True)
		books = Schedule.objects.filter(date = day_obj,coach__in = coaches)
		#print books.query
		return (books.count(),self.cal_course_income(books),self.cal_exp_course_count(books))


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
		course_count, course_price, exp_course_count = self.sum_price_course(gymid, day)
		return Response({"sold_price": sold_price, "sold_count":sold_count, "course_price":course_price, "course_count": course_count, "exp_course_count":exp_course_count})

class GymTrialCustomerList(generics.ListAPIView):
	serializer_class = SimpleUserSerilaizer
	pagination_class = None
	def get_queryset(self):
		ret = User.objects.filter(trial = self.kwargs['gymid'])
		return ret


class GymCustomers(generics.ListAPIView):
	pagination_class = None
	serializer_class = SimpleUserSerilaizer
	def get_queryset(self):
		gym = Gym.objects.get(id=self.kwargs["gymid"])
		customlist = gym.get_all_customers()
		customlist = list(set(customlist))
		ret = User.objects.filter(name__in = customlist)
		return ret

class GymCustomersFreuently(APIView):
    def get(self, request, gymid):
	gym = Gym.objects.get(id=self.kwargs["gymid"])
	customlist = gym.get_all_customers()
        ret = []
        duration = int(request.GET['duration'])
        if 'greaterthan' in request.GET:
            limit = int(request.GET['greaterthan'])
            for c in customlist:
                u = get_object_or_404(User,name=c)
                if u.get_frequency(duration) >= limit:
                    ret.append(u.displayname)
        if 'equal' in request.GET:
            limit = int(request.GET['equal'])
            for c in customlist:
                u = get_object_or_404(User,name=c)
                if u.get_frequency(duration) == limit:
                    ret.append(u.displayname)
        html = render(request, "private/customerlist.html",{'customers': ret})
	return html



def alipay_success(request):
	#http://182.92.203.171/pay/success/?result=success&out_trade_no=1457523599263297
	if request.GET["result"] != "success":
		return render(request, "payfail.html")
	orderid = request.GET["out_trade_no"]
	order = get_object_or_404(Order,billid=orderid)
	'''
	order.status = "paid"
	order.save()
	'''
	print order.custom
	auth_usr = get_user_model().objects.create_user(username=order.custom.name)
	pwd = randint(100000,999999)
	auth_usr.set_password(pwd)
	auth_usr.save()
	jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
	jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
	payload = jwt_payload_handler(auth_usr)
	token = jwt_encode_handler(payload)
	ret = render(request, "paysuccess.html",{"username":auth_usr.username,"pwd":pwd,"token":token})
	ret.set_cookie("token", token)
	ret.set_cookie("user",auth_usr.username)
	return ret

class GymBackup(generics.ListAPIView):
	pagination_class = None
	serializer_class = GymBackupSerilaizer
	def get_queryset(self):
            orders = Order.objects.filter(gym=get_object_or_404(Gym,id=self.kwargs['gymid']))
            return orders



def sendmail(gymid, mails):
        orders = Order.objects.filter(gym=get_object_or_404(Gym,id=gymid)).annotate(test=Sum('amount'))
        return Response(orders)
#                .extra({'paidday': "date_format(date(CONVERT_TZ(`paidtime`,'+00:00','+08:00')),'%%Y%%m%%d')"}) \
                
                

        '''
        rows = []
        for order in orders:
            row = []
            row.append(str(order.custom.displayname))
            row.append(str(order.custom.name))
            row.append(str(order.paidtime))
            row.append(str(order.amount))
            coursecount = str(order.product.amount)
            completed = str(order.schedule_set.filter(done=1).count())
            row.append(str(coursecount) + '/' + str(completed))
            rows.append("\t".join(row))
            break
        #send mail
        body = "\n".join(rows)
        command = 'echo "%s"| mail -s "Backup(o2-fit.com)" %s' % (body, ' '.join(mails))
        print command
        os.system(command)
        '''


            


def backup_order(request):
    #1.get
    gid = 19
    return sendmail(gid, ['1325990578@qq.com'])


class GymSaleDetail(generics.ListAPIView):
	serializer_class = OrderSerializer
	pagination_class = None
	def get_queryset(self):
		if "end" in self.request.GET:
			end = datetime.datetime.strptime(self.request.GET["end"], "%Y%m%d")
		else:
			end = datetime.date.today()

		if "start" in self.request.GET:
			start = datetime.datetime.strptime(self.request.GET["start"], "%Y%m%d")
		else:
		        start = end - datetime.timedelta(days=365)

		end = end + datetime.timedelta(days=1)

		orders = Order.objects.filter(gym=get_object_or_404(Gym,id=self.kwargs.get('pk')),paidtime__range=[start,end]) \
				.extra({'paidday': "date_format(date(CONVERT_TZ(`paidtime`,'+00:00','+08:00')),'%%Y%%m')"})
		return orders

class DeadOrderList(generics.ListAPIView):
	serializer_class = OrderSerializer 
	pagination_class = None
	def get_queryset(self):
		gym = get_object_or_404(Gym, id=self.kwargs.get("pk"))
		orders = gym.orders.exclude(status__in=["unpaid","done"])
		today = datetime.datetime.today().date()
		enddate = datetime.datetime.today().date() + datetime.timedelta(days=10)
                ret = []
                for order in orders:
                    ed = order.cal_endtime()
                    if ed == 'N/A':
                        continue
                    d = datetime.datetime.strptime(ed, "%Y-%m-%d").date()
                    if d >= today and d <= enddate:
                        ret.append(order)
		return ret

