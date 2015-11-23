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


# Create your views here.


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
		print date_str
		return get_object_or_404(Schedule,coach=coach,date=date_str, hour=hour)

	def partial_update(self, request, *args, **kwargs):
		print request.DATA
		ret = super(ScheduleItem, self).partial_update(request, args,kwargs)
		if 'rate' in request.DATA:
			print "rating ... ..."
			print request.DATA
			order = Order.objects.get(id=request.DATA["order"])
			coach = User.objects.get(id=order.coach.id)
			print coach
			#coach = get_object_or_404(User, order.coach.name)
			coach.rate += request.DATA["rate"]
			coach.course_count += 1
			print "..............."
			print coach.course_count
			coach.save()
			print "xxxxxxxxxxxxxxx"
		if "order" in request.DATA:
			order = Order.objects.get(id=request.DATA["order"])
			coach = User.objects.get(id=order.coach.id)
			ordered_count = Schedule.objects.filter(order=request.DATA["order"],deleted=False,done=True).count()
			order_count = order.product.amount
			if ordered_count == order_count:
				order.status = "done" 
				order.save()
			#update course count and order_count
			coach.course_count = Schedule.objects.filter(deleted=False,done=True).count()
			coach.order_count = Order.objects.get(coach=coach).count()
			coach.save()
		return ret



class ScheduleList(generics.ListCreateAPIView):
	pagination_class = None
	serializer_class = ScheduleSerializer 
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
	def create(self, request, *args, **kwargs):
		print json.dumps(request.data)
		ret = super(ScheduleList, self).create(request, args,kwargs)
		print request.data["order"]
		order = Order.objects.get(id=request.data["order"])
		ordered_count = Schedule.objects.filter(order=request.data["order"],deleted=False).count()
		order_count = order.product.amount
		if order.status == "paid" and ordered_count == order_count:
			order.status = "inprogress" 
			order.save()
		return ret

class ScheduleForReadPagination(pagination.CursorPagination):
	ordering = 'date'

class ScheduleForRead(generics.ListAPIView):
	serializer_class = ScheduleSerializer 
	def list(self, request, *args, **kwargs):
		duration = 7
		usr = get_object_or_404(User, name=self.kwargs.get("name"))
		startdate = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		enddate = startdate + datetime.timedelta(days=duration)

		#mindate = startdate - datetime.timedelta(days=40)
		maxdate = startdate + datetime.timedelta(days=40)

		queryset = None
		while(True):
			daterange = [startdate, enddate]
			if usr.iscoach:
				queryset = Schedule.objects.filter(coach=usr.id, date__range=daterange).order_by("date","hour")
			else:
				queryset = Schedule.objects.filter(custom=usr.id, date__range=daterange).order_by("date","hour")
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

class DayAvaiableTime(APIView):
	def get(self,request,name,date):
		coach = get_object_or_404(User, name=self.kwargs.get("name"))
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")

		workingday = get_object_or_404(WorkingDays, name=self.kwargs.get("name"))
		working = map(lambda x: datetime.datetime.strptime(x,"%Y/%m/%d"),
				filter(bool, workingday.excep_work.split("|")))
		rest = map(lambda x: datetime.datetime.strptime(x,"%Y/%m/%d"),
				filter(bool, workingday.excep_rest.split("|")))
		weekrest = []
		outhours = []
		noonhours = []
		if len(workingday.weekrest) != 0:
			weekrest = workingday.weekrest.split("|")
		if len(workingday.out_hours) != 0:
			outhours = workingday.out_hours.split("|")
		if len(workingday.noon_hours) != 0:
			noonhours = map(lambda x: int(x), workingday.noon_hours.split("|"))

		#print "weekdays: " + str(date.weekday())
		#print "weekdays: " + str((date.weekday() + 1)%7)
		print working

		out = map(lambda x: int(x), outhours)
		ava = [h for h in range(0,26) if not h in out]
		#print date
		#print datetime.datetime.today()
	
		if ((str((date.weekday() + 1)%7) in weekrest) and (not date in working)) or (date in rest):
			ret = {"out":out,"na": ava,"availiable":[], "noon":noonhours}
			return Response(ret, status=status.HTTP_200_OK)

		#get all booked hour
		booked = Schedule.objects.filter(coach=coach.id, date=date)
		na = []
		for b in booked:
			na.append(b.hour)
			na.append(b.hour + 1)
		na = na + noonhours
		ava = [h for h in ava if h not in na]
		ret = {"out":out,"na": na,"availiable":ava, "noon":noonhours}
		return Response(ret, status=status.HTTP_200_OK)

@permission_classes((AllowAny, ))
class AllEvalOptionsView(generics.ListCreateAPIView):
	queryset = BodyEvalOptions.objects.all()
	serializer_class = BodyEvalOptionsSerializer
	pagination_class = None


class BodyEvalDateView(generics.ListAPIView):
	pagination_class = None
	serializer_class = BodyEvalDateSerializer 
	def get_queryset(self):
		return BodyEval.objects.filter(name=self.kwargs.get("name")).values('date').distinct()


class BodyEvalByDateView(ListBulkCreateAPIView):
	pagination_class = None
	serializer_class = BodyEvalSerializer
	def get_queryset(self):
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		date_str = datetime.datetime.strftime(date,"%Y-%m-%d")
		name = self.kwargs.get("name")
		return BodyEval.objects.filter(date=date_str, name=name)

class TrainDateView(generics.ListAPIView):
	pagination_class = None
	serializer_class = TrainDateSerializer 
	def add_months(self, sourcedate,months):
		month = sourcedate.month - 1 + months
		year = int(sourcedate.year + month / 12 )
		month = month % 12 + 1
		day = min(sourcedate.day,calendar.monthrange(year,month)[1])
		return datetime.date(year,month,day)
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
		return Train.objects.filter(date=date_str, name=name)

	def create(self, request, *args, **kwargs):
		bulk = isinstance(request.DATA, list)
		ret = super(TrainByDateView, self).create(request, *args, **kwargs)
		print("xxxxxxxxxxxxxxxxxxxx")
		scheduleid = -1

		if bulk and "course" in request.DATA[0]:
			scheduleid = request.DATA[0]["course"]
		if not bulk and "course" in request.DATA:
			scheduleid = request.DATA["course"]
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
		
		
		





