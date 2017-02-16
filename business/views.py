# coding=utf-8
from django.shortcuts import render
from business.models import *
from business.serializers import *
from order.models import *
from usr.models import *
from rest_framework import generics,pagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import render,get_object_or_404,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
import time
from pytz import timezone
from rest_framework_bulk import ListBulkCreateAPIView 
import requests
import calendar
from django.conf import settings
import json
from django.http import JsonResponse


# Create your views here.

class FinanceList(generics.ListCreateAPIView):
	serializer_class = FinanceSerializer
	pagination_class = None

        def get_queryset(self):
            #1 get date range
            startdate = self.request.GET["start"]
            enddate = self.request.GET["end"]
            pk = self.kwargs.get("pk")

            startday = datetime.datetime.strptime(startdate,"%Y%m%d")
            endday = datetime.datetime.strptime(enddate,"%Y%m%d")
            
            #2 get all schedule
            allitems = Finance.objects.filter(gym=int(pk), date__range=[ startday, endday])
            #3 cal
            return allitems

class FlowList(generics.ListCreateAPIView):
	serializer_class = FlowSerializer
	pagination_class = None

        def get_queryset(self):
            #1 get date range
            startdate = self.request.GET["start"]
            enddate = self.request.GET["end"]
            pk = self.kwargs.get("pk")

            startday = datetime.datetime.strptime(startdate,"%Y%m%d")
            endday = datetime.datetime.strptime(enddate,"%Y%m%d")
            
            #2 get all schedule
            allitems = Flow.objects.filter(gym=int(pk), date__range=[ startday, endday])
            #3 cal
            return allitems



class FinanceItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = Finance.objects.all()
	serializer_class = FinanceSerializer

class FlowItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = Flow.objects.all()
	serializer_class = FlowSerializer

class FlowItemByDate(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = FlowSerializer
        def get_object(self):
            d = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
            gymid = self.kwargs.get("gymid")
            ret, _ = Flow.objects.get_or_create(gym=gymid, date = d)
            return ret


class CourseList(generics.ListCreateAPIView):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	pagination_class = None


class CourseItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer

class GymList(generics.ListCreateAPIView):
	queryset = Gym.objects.all()
	serializer_class = GymSerializer
	pagination_class = None

class GymItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = Gym.objects.all()
	serializer_class = GymSerializer

class ScheduleItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = Schedule.objects.all()
	serializer_class = ScheduleSerializer 
	def get_object(self):
		coach = get_object_or_404(User, name=self.kwargs.get("name"))

		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		date_str = datetime.datetime.strftime(date,"%Y-%m-%d")
		hour  = self.kwargs.get("hour")
		ret = Schedule.objects.filter(coach=coach,date=date_str, hour=hour).first()
		return ret
		#return get_object_or_404(Schedule,coach=coach,date=date_str, hour=hour)

	def partial_update(self, request, *args, **kwargs):
		ret = super(ScheduleItem, self).partial_update(request, args,kwargs)
		if 'rate' in request.data:
			print "rating ... ..."
			coach = self.get_object().coach
			print coach
			#coach = get_object_or_404(User, order.coach.name)
			coach.rate += request.DATA["rate"]
			coach.save()

                if request.data["done"] or "order" in request.data:
                        self.get_object().doneBook()
                        self.get_object().create_threshold_msg()
		return ret

class GymScheduleList(generics.ListAPIView):
	pagination_class = None
	serializer_class = ScheduleSerializer 
	def get_queryset(self):
		gym = get_object_or_404(Gym, id=self.kwargs.get("pk"))
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		queryset = Schedule.objects.filter(coach__in=gym.coaches.values_list("id",flat=True), date=date).order_by("hour")
		return queryset

class GymLoadList(APIView):
        def get(self, request, pk, date):
	    gym = get_object_or_404(Gym, id=self.kwargs.get("pk"))
	    date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
	    queryset = Schedule.objects.filter(coach__in=gym.coaches.values_list("id",flat=True), date=date).order_by("hour")
            #init
            ret = []
            for i in range(0,26):
                ret.append({'hour':i,'course_count':0})

            for hour in queryset:
                ret[hour.hour]['course_count'] += 1
                ret[hour.hour+1]['course_count'] += 1

	    return Response(ret, status=status.HTTP_200_OK)

               
        


class ScheduleList(generics.ListCreateAPIView):
	pagination_class = None
	serializer_class = ScheduleSerializer 
	def get_queryset(self):
		coach = get_object_or_404(User, name=self.kwargs.get("name"))
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		queryset = Schedule.objects.filter(coach=coach.id, 
				date=date).order_by("hour")
		return queryset
	'''
	def get_queryset(self):
		coach = get_object_or_404(User, name=self.kwargs.get("name"))
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		#filter 
		workingday = get_object_or_404(WorkingDays, name=self.kwargs.get("name"))
		working = map(lambda x: datetime.datetime.strptime(x,"%Y/%m/%d"),
				filter(bool, workingday.excep_work.split("|")))
		rest = map(lambda x: datetime.datetime.strptime(x,"%Y/%m/%d"),
				filter(bool, workingday.excep_rest.split("|")))
		weekrest = workingday.weekrest.split("|")
		if not (date.weekday() + 1)%7 in weekrest:
			working.append(date)
		queryset = Schedule.objects.filter(coach=coach.id, 
				date=date,
				date__in=working
				).exclude(date__in=rest).order_by("hour")
		return queryset
	'''
	def create(self, request, *args, **kwargs):
		print json.dumps(request.data)
		#ret = super(ScheduleList, self).create(request, args,kwargs)
		customer = User.objects.get(id=request.data["custom"])
		coach = User.objects.get(id=request.data["coach"])
                order = None
                if "order" in request.data:
         		order = Order.objects.get(id=request.data["order"])
		book = Schedule.objects.create(coach=coach,
				custom=customer,
				date= datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d").date(),
				hour=request.data["hour"],
				order=order)
		if "done" in request.data:
			book.done = request.data["done"]
			book.save()
                        # threshold mesg
		sl = ScheduleSerializer(instance=book)
		print sl.data
                #if is an order book
                if "order" in request.data:
     		        ordered_count = Schedule.objects.filter(order=request.data["order"],deleted=False).count()
		        order_count = order.product.amount
		        if order.status == "paid" and ordered_count == order_count:
		                order.status = "inprogress" 
		                order.save()
		#send sms
                customer.trySendEvalNotification(book)
                book.send_launch_notification()
		#print book.sendSms()
		return Response(sl.data)

class ScheduleForReadPagination(pagination.CursorPagination):
	ordering = 'date'

class ScheduleForReadQuery(generics.ListAPIView):
        pagination_class = None
	serializer_class = ScheduleSerializer 
	def get_queryset(self):
		usr = get_object_or_404(User, name=self.kwargs.get("name"))
	        startdate = datetime.datetime.strptime(self.request.GET["start"],"%Y%m%d")
	        enddate = datetime.datetime.strptime(self.request.GET["end"],"%Y%m%d")
		daterange = [startdate, enddate]
                print startdate
                print enddate
		return usr.sealed_time.filter(date__range=daterange).order_by("date","hour")




class ScheduleForRead(generics.ListAPIView):
	serializer_class = ScheduleSerializer 
	def list(self, request, *args, **kwargs):
		duration = 6
		usr = get_object_or_404(User, name=self.kwargs.get("name"))
		startdate = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		enddate = startdate + datetime.timedelta(days=duration)

		#mindate = startdate - datetime.timedelta(days=40)
		maxdate = startdate + datetime.timedelta(days=40)

		queryset = None
		while(True):
			daterange = [startdate, enddate]
			if usr.iscoach:
				queryset = usr.sealed_time.filter(date__range=daterange).order_by("date","hour")
			else:
				queryset = usr.booked_time.filter(date__range=daterange).order_by("date","hour")
			#startdate = startdate - datetime.timedelta(days=duration)
			enddate = enddate + datetime.timedelta(days=duration)
			if queryset.count() > 5 or enddate>maxdate:
				break

		baseUrl = request.build_absolute_uri()[:-9]
		nextstart = baseUrl + datetime.date.strftime(enddate + datetime.timedelta(days=1), "%Y%m%d") + "/"
		prevstart = baseUrl + datetime.date.strftime(startdate - datetime.timedelta(days=duration+1),"%Y%m%d") + "/"
		if startdate > datetime.datetime.today() + datetime.timedelta(days=31):
			nextstart = None
		serializer = self.get_serializer(queryset, many=True)
		return Response({"next":nextstart,"previous":prevstart, "results":serializer.data})
class CustomerMonthAverageView(APIView):
	def get(self,request,pk,date):
            #1 get date range
            date += "01"
            startday = datetime.datetime.strptime(date,"%Y%m%d")
	    endday = startday + datetime.timedelta(days=30)
            
            #2 get all schedule
	    gym = get_object_or_404(Gym, id=pk)
            allschedule = Schedule.objects.filter(coach__in=gym.coaches.values_list("id",flat=True),done=True,date__range=[ startday, endday])
            #3 cal
            customer_count = allschedule.values("custom").distinct().count()
            return Response({"course_count":allschedule.count(), "customer_count":customer_count, "average":float(allschedule.count())/float(customer_count)})

def add_months(sourcedate,months):
        month = sourcedate.month - 1 + months
	year = int(sourcedate.year + month / 12 )
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return datetime.date(year,month,day)


def customer_month_detail_view(request, date, pk):
        date += "01"
        startday = datetime.datetime.strptime(date,"%Y%m%d")
	endday = add_months(startday,1) - datetime.timedelta(days=1)
            
            #2 get all schedule
	gym = get_object_or_404(Gym, id=pk)
        allschedule = Schedule.objects.filter(coach__in=gym.coaches.values_list("id",flat=True),done=True,date__range=[ startday, endday])
        for item in allschedule:
            item.customername = item.custom.displayname

        ret = render(request, "analyse/customermonthdetail.html",{'allschedules':allschedule})
        return ret



class CustomerMonthDetailView(generics.ListAPIView):
	serializer_class = ScheduleCustomerBriefSerializer
        pagination_class = None
	def add_months(self, sourcedate,months):
		month = sourcedate.month - 1 + months
		year = int(sourcedate.year + month / 12 )
		month = month % 12 + 1
		day = min(sourcedate.day,calendar.monthrange(year,month)[1])
		return datetime.date(year,month,day)

        def get_queryset(self):
            #1 get date range
            date = self.kwargs.get("date")
            pk = self.kwargs.get("pk")
            date += "01"
            startday = datetime.datetime.strptime(date,"%Y%m%d")
	    endday = self.add_months(startday,1) - datetime.timedelta(days=1)
            
            #2 get all schedule
	    gym = get_object_or_404(Gym, id=pk)
            allschedule = Schedule.objects.filter(coach__in=gym.coaches.values_list("id",flat=True),done=True,date__range=[ startday, endday])
            #3 cal
            return allschedule

            

class DayAvaiableTime(APIView):

	def getDayAva(self, coachname, date):
		#date = datetime.datetime.strptime(datestr,"%Y%m%d")

		coach = get_object_or_404(User, name=coachname)
		workingday = get_object_or_404(WorkingDays, name=coachname)
		working = map(lambda x: datetime.datetime.strptime(x,"%Y/%m/%d"),
				filter(bool, workingday.excep_work.split("|")))
		rest = map(lambda x: datetime.datetime.strptime(x,"%Y/%m/%d"),
				filter(bool, workingday.excep_rest.split("|")))

		print "1"
		weekrest = []
		outhours = []
		noonhours = []
		if len(workingday.weekrest) != 0:
			weekrest = workingday.weekrest.split("|")
		if len(workingday.out_hours) != 0:
			outhours = workingday.out_hours.split("|")
		if len(workingday.noon_hours) != 0:
			noonhours = map(lambda x: int(x), workingday.noon_hours.split("|"))

		out = map(lambda x: int(x), outhours)
		ava = [h for h in range(0,26) if not h in out]
	
		if ((str((date.weekday() + 1)%7) in weekrest) and (not date in working)) or (date in rest):
			ret = {"out":out,"na": ava,"availiable":[], "noon":noonhours}
			return ret

		booked = Schedule.objects.filter(coach=coach.id, date=date)
		na = []
		for b in booked:
			na.append(b.hour)
			na.append(b.hour + 1)
		na = na + noonhours
		ava = [h for h in ava if h not in na]
		ret = {"out":out,"na": na,"availiable":ava, "noon":noonhours}
		return ret

	def get(self,request,name,date):
		print request.query_params
		curdate = datetime.datetime.strptime(date,"%Y%m%d")
		if "days" in request.query_params:
			ret = []
			#build the week
			for i in range(0,int(request.query_params["days"])):
				tmpday = curdate + datetime.timedelta(days=i)
				tmp = self.getDayAva(name, tmpday)
				tmp["date"] = datetime.datetime.strftime(tmpday, "%Y%m%d")
				ret.append(tmp)
		else :
			ret = self.getDayAva(name,curdate)
		return Response(ret, status=status.HTTP_200_OK)

class TrialBookView(generics.ListCreateAPIView):
	pagination_class = None
	serializer_class = ScheduleSerializer 
        def get_queryset(self):
		customer = User.objects.get(name=self.kwargs.get("name"))
                return customer.booked_time.filter(order=None)

@permission_classes((AllowAny, ))
class AllEvalOptionsView(generics.ListCreateAPIView):
	queryset = BodyEvalOptions.objects.all()
	serializer_class = BodyEvalOptionsSerializer
	pagination_class = None

class BodyEvalItemView(generics.RetrieveDestroyAPIView):
	queryset = BodyEval.objects.all()
	serializer_class = BodyEvalDateSerializer


class BodyEvalDateView(generics.ListAPIView):
	pagination_class = None
	serializer_class = BodyEvalDateSerializer 
	def get_queryset(self):
		return BodyEval.objects.filter(name=self.kwargs.get("name")).values('date').distinct()

class BodyEvalAllView(generics.ListAPIView):
	pagination_class = None
	serializer_class = BodyEvalSerializer
	def get_queryset(self):
		return BodyEval.objects.filter(name=self.kwargs.get("name")).order_by("date")


class BodyEvalByOptionView(generics.ListAPIView):
	pagination_class = None
	serializer_class = BodyEvalSerializer
	def get_queryset(self):
                option = self.kwargs.get("option")
		return BodyEval.objects.filter(name=self.kwargs.get("name"),option=option).order_by("-date")



class BodyEvalByDateView(ListBulkCreateAPIView):
	pagination_class = None
	serializer_class = BodyEvalSerializer
	def get_queryset(self):
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		date_str = datetime.datetime.strftime(date,"%Y-%m-%d")
		name = self.kwargs.get("name")
		return BodyEval.objects.filter(date=date_str, name=name)

@permission_classes((AllowAny, ))
class AllHealthQuesOptionsView(generics.ListCreateAPIView):
	queryset = HealthQuesOptions.objects.all()
	serializer_class = HealthQuesOptionsSerializer
	pagination_class = None


class HealthQuesDateView(generics.ListAPIView):
	pagination_class = None
	serializer_class = HealthQuesDateSerializer 
	def get_queryset(self):
		return HealthQues.objects.filter(name=self.kwargs.get("name")).values('date').distinct()


class HealthQuesByDateView(ListBulkCreateAPIView):
	pagination_class = None
	serializer_class = HealthQuesSerializer
	def get_queryset(self):
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		date_str = datetime.datetime.strftime(date,"%Y-%m-%d")
		name = self.kwargs.get("name")
		return HealthQues.objects.filter(date=date_str, name=name)



class TrainDateView(generics.ListAPIView):
	pagination_class = None
	serializer_class = TrainDateSerializer 
	def add_months(self, sourcedate,months):
		month = sourcedate.month - 1 + months
		year = int(sourcedate.year + month / 12 )
		month = month % 12 + 1
		day = min(sourcedate.day,calendar.monthrange(year,month)[1])
		return datetime.date(year,month,day)
	'''
	def list(self, request, *args, **kwargs):
		#1. set start date
		month = datetime.date.today()
		month = datetime.date(month.year, month.month, 1)
		if "month" in request.GET:
			month = datetime.datetime.strptime(request.GET["month"],"%Y%m")
		qc = Train.objects.filter(name=self.kwargs.get("name"), date__year=month.year, date__month=month.month).values('date').distinct().order_by("-date")
		serializer = self.get_serializer(qc, many=True)
		print serializer.data
		baseUrl =  "http://" + request.get_host() + request.path
		nextstart = datetime.date.strftime(self.add_months(month, 1), "%Y%m")
		prevstart = datetime.date.strftime(self.add_months(month, -1),"%Y%m")
		return Response({
			"next": baseUrl + "?month="+nextstart,
			"previous": baseUrl + "?month="+prevstart,
			"results": serializer.data
			})
	'''
	def get_queryset(self):
		return Train.objects.filter(name=self.kwargs.get("name")).values('date').distinct().order_by('-date')

@permission_classes((AllowAny, ))
class TrainByDateView(ListBulkCreateAPIView):
	pagination_class = None
	serializer_class = TrainSerializer
	def get_queryset(self):
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		date_str = datetime.datetime.strftime(date,"%Y-%m-%d")
		name = self.kwargs.get("name")
		return Train.objects.filter(date=date_str, name=name).order_by("action_order", "groupid")

	def create(self, request, *args, **kwargs):
		bulk = isinstance(request.data, list)
		ret = super(TrainByDateView, self).create(request, *args, **kwargs)
		scheduleid = -1

		if bulk and "course" in request.data[0]:
			scheduleid = request.data[0]["course"]
		if not bulk and "course" in request.data:
			scheduleid = request.data["course"]

		if scheduleid != -1:
			schedule = get_object_or_404(Schedule,id=scheduleid)
			schedule.done = True
			schedule.save()
		return ret
class TrainByScheduleView(generics.ListAPIView):
	pagination_class = None
	serializer_class = TrainSerializer
	def get_queryset(self):
		#date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		#date_str = datetime.datetime.strftime(date,"%Y-%m-%d")
		name = self.kwargs.get("name")
		return Train.objects.filter(name=name,  course=self.kwargs.get("schedule"))

class TrainItemView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Train.objects.all()
	serializer_class = TrainSerializer


#class NearByView(generics.ListAPIView):

class NearByView(APIView):
	#pagination_class = None
	serializer_class = GymSerializer
	def get(self,request):
		#http://yuntuapi.amap.com/datasearch/around?key=a2be60fd9e30425d8e7c003ba81a1f12&center=116.28113,40.03241&tableid=560353bae4b0fe6c79f8f0d0
		key = settings.GAODE_KEY
		tableid = settings.GAODE_TABLEID
		url = settings.GAODE_URL
		#print self.request.GET
		loc = str(request.GET["longitude"]) + "," + str(request.GET["latitude"])
		params = {
				"key":key,
				"tableid":tableid,
				"center": loc,
				"sortrule": "_distance"
				}
		resp = requests.get(url,params=params).json()
		gymlist = []
		dislist = {}
		for gym in resp["datas"]:
			gymlist.append(gym["_id"])
			dislist[gym["_id"]] = int(gym["_distance"])
		ret =  Gym.objects.filter(mapid__in = gymlist)
		allgym = []
		for item in ret:
			item.distance = dislist[str(item.mapid)]
			print item.distance
			allgym.append(item)
		#print ret[0].distance
		serializer = GymSerializer(allgym, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
class GymMap(APIView):
	def get(self,request, pk):
		_id = get_object_or_404(Gym, id=pk).mapid
		#http://restapi.amap.com/v3/staticmap?markers=mid,0xFF0000,:116.37359,39.92437&key=a2be60fd9e30425d8e7c003ba81a1f12
		#get locaction by id
		#http://yuntuapi.amap.com/datasearch/id?tableid=52b155b6e4b0bc61deeb7629&_id=372&key=

		key = settings.GAODE_KEY
		tableid = settings.GAODE_TABLEID
		queryurl = "http://yuntuapi.amap.com/datasearch/id"
		mapurl = "http://restapi.amap.com/v3/staticmap"
		params = {
				"key":key,
				"tableid":tableid,
				"_id": _id,
				}
		print params
		resp = requests.get(queryurl, params).json()
		if resp["info"] != "OK":
			return Response({resp["info"]}, status=status.HTTP_400_BAD_REQUEST)
		loc = resp["datas"][0]["_location"]
		ret = mapurl + "?markers:mid,0xFF0000,:" + loc + "&key=" + key	
		return redirect(ret)
		
class GymIncompleteList(generics.ListAPIView):
	serializer_class = ScheduleSimpleSerializer
	pagination_class = None
	def get_queryset(self):
		gym = get_object_or_404(Gym, id=self.kwargs.get("pk"))
		orders = gym.orders.exclude(status__in=["unpaid","done"]).values_list("id", flat=True)
		print orders
		today = datetime.datetime.today().date()
		ret = Schedule.objects.filter(date__lt=today,done=False,order__in=orders).order_by("date","hour")
		return ret

class CoachIncompleteList(generics.ListAPIView):
	serializer_class = ScheduleSerializer
	pagination_class = None
	def get_queryset(self):
		usr = get_object_or_404(User, name=self.kwargs.get("name"))
		orders = usr.income_orders.exclude(status__in=["unpaid","done"]).values_list("id", flat=True)
		today = datetime.datetime.today().date()
                print today
		ret = Schedule.objects.filter(date__lt=today,done=False,order__in=orders).order_by("date","hour")
                print ret.query
		return ret

		
		
class GymSumSale(APIView):	
	def get(self,request,pk):
		gym = get_object_or_404(Gym, id=pk)
		sum_coursecount = 0
                sum_completedcount = 0
		for o in gym.orders.iterator():
			sum_coursecount += o.product.amount
                        sum_completedcount += o.schedule_set.count()
		#sum_completedcount = Schedule.objects.filter(coach__in=gym.coaches.values_list("id",flat=True), done=True).count()
		return Response({"sum_coursecount":sum_coursecount, "sum_completedcount": sum_completedcount})
		


def show_customer_eval(request, name):
        opts = {}
        print name
        user = get_object_or_404(User,name=name)
        startday = datetime.datetime.today() + datetime.timedelta(days=-30)
        times = user.booked_time.filter(date__gt=startday).count()
        lastevalday = BodyEval.objects.filter(name=name).order_by('-date')[0].date
        lastevalday_str = datetime.datetime.strftime(lastevalday,"%Y-%m-%d")

        evals = BodyEval.objects.filter(name=name).values_list('option', flat=True).distinct()
        deltas = []
        for ev in evals:
            evs = BodyEval.objects.filter(name=name,option=ev).order_by('-date')
            if evs.count() < 2:
                continue
            delta = float(evs[0].value) - float(evs[1].value)
            d0 = datetime.datetime.strftime(evs[0].date, "%m/%d")
            d1 = datetime.datetime.strftime(evs[1].date, "%m/%d")
            deltas.append({'d0':d0, 'd1':d1,'delta': delta,'option':ev,'prev':evs[1].value,'current':evs[0].value,'unit':evs[0].unit})
        ret = render(request, "evalresult/report.html",{'avatar': user.avatar, "deltas":deltas, "lastevalday":lastevalday_str,"name":name, "times":times})
        return ret



def show_gesture_eval(request, name):
        user = get_object_or_404(User,name=name)
        lastevalday = BodyEval.objects.filter(name=name).order_by('-date')[0].date
        evals = BodyEval.objects.filter(name=name, date=lastevalday).order_by("value")

        issues = []
        for item in evals:
            if item.group.startswith("3.") or item.group.startswith("4.") or item.group.startswith("5."):
                if int(item.value) < 10:
                    if item.img is None:
                        item.img = ""
                    if item.comments is None or item.comments == '':
                        item.comments = "暂无建议"

                    if item.risks is None or item.risks == '':
                        item.risks = ""
                    else:
                        item.risks = item.risks.split(",")

                    issues.append(item)
        
        ret = render(request, "evalresult/gesture.html",{"issues":issues})
        return ret

def get_health_risk(request):
        risk = ["腰痛","背痛","颈肩痛","便秘","手脚麻","头晕","头痛","骨刺","颈椎退化","耳鸣","身体疲倦","眼睛干涩","脊柱变型","失眠","膝关节痛","腰椎间盘突出"]
        return JsonResponse(dict(risks=list(risk)))

class GymGroupCourseList(generics.ListCreateAPIView):
	serializer_class = GroupCourseSerializer
	pagination_class = None
        lookup_field = "gym"
	def get_queryset(self):
		ret = GroupCourse.objects.filter(gym=self.kwargs.get("pk"))
		return ret

class CustomerGroupCourseList(generics.ListCreateAPIView):
	serializer_class = GroupCourseInstanceBookDetailSerializer
	pagination_class = None
	def get_queryset(self):
		ret = GroupCourseInstanceBook.objects.filter(customer=self.kwargs.get("name"))
		return ret

#TODO
class GymGroupCourseDayList(generics.ListCreateAPIView):
	serializer_class = GroupCourseInstanceSerializer
	pagination_class = None
	def get_queryset(self):
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		ret = GroupCourseInstance.objects.filter(gym=self.kwargs.get("pk"),date=date.date())
		return ret

class GroupCourseItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = GroupCourse.objects.all()
	serializer_class = GroupCourseSerializer

class GroupCourseBookItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = GroupCourseInstanceBook.objects.all()
	serializer_class = GroupCourseInstanceBookSerializer

class GroupCourseInstanceItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = GroupCourseInstance.objects.all()
	serializer_class = GroupCourseInstanceSerializer


class GroupCourseInstanceList(generics.ListCreateAPIView):
	serializer_class = GroupCourseInstanceSerializer
	pagination_class = None
	def get_queryset(self):
                ret = GroupCourseInstance.objects.filter(gym=self.kwargs.get("pk"))
                return ret


class GymGroupCourseDayBookList(generics.ListCreateAPIView):
	serializer_class = GroupCourseInstanceBookSerializer
	pagination_class = None
	def get_queryset(self):
		gym = get_object_or_404(Gym, id=self.kwargs.get("pk"))
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		ret = GroupCourseInstanceBook.objects.filter(date=date.date(), gym=self.kwargs.get("pk"))
		return ret

	def create(self, request, *args, **kwargs):
		ret = super(GymGroupCourseDayBookList, self).create(request, args,kwargs)
                return ret
                #create consumption log


class UserSummaryView(APIView):
        def get(self, request, name):
            usr = get_object_or_404(User, name=name)
            #get pt count
            pt = Schedule.objects.filter(custom=usr,done=True)
            pt_count = pt.count()

            #get groupcourse count
            gc = GroupCourseInstanceBook.objects.filter(customer=name,date__lte=datetime.datetime.today())
            gc_count = gc.count()

            endday = datetime.datetime.today() + datetime.timedelta(days=-7)

            week_trained = 0
            for item in gc:
                if item.date > endday.date():
                    week_trained += 1

            for item in pt:
                if item.date > endday.date():
                    week_trained += 1


            ret = {"name":usr.name,\
                    "displayname":usr.displayname,\
                    "balance":usr.balance,\
                    "pt_count":pt_count,\
                    "gc_count":gc_count,\
                    "week_trained":week_trained,\
                    "discount":get_discount(usr.name)}
            #get
            return Response(ret, status=status.HTTP_200_OK)

def get_discount(name):

            usr = get_object_or_404(User, name=name)

            pt = Schedule.objects.filter(custom=usr,done=True)

            #get groupcourse count
            gc = GroupCourseInstanceBook.objects.filter(customer=name,date__lte=datetime.datetime.today())

            endday = datetime.datetime.today() + datetime.timedelta(days=-7)

            week_trained = 0
            for item in gc:
                if item.date > endday.date():
                    week_trained += 1

            for item in pt:
                if item.date > endday.date():
                    week_trained += 1
            if week_trained >= 3:
                return 15
            if week_trained >= 2:
                return 10
            return 0

            

