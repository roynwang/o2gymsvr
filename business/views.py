from django.shortcuts import render
from business.models import *
from business.serializers import *
from order.models import *
from usr.models import *
from rest_framework import generics,pagination
from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
import time
from pytz import timezone
from rest_framework_bulk import ListBulkCreateAPIView 


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
		ret = super(ScheduleItem, self).partial_update(request, args,kwargs)
		if 'rate' in request.DATA:
			print "rating ... ..."
			print request.DATA
			order = Order.objects.get(id=request.DATA["order"])
			ordered_count = Schedule.objects.filter(order=request.DATA["order"],deleted=False,done=True).count()
			order_count = order.product.amount
			if ordered_count == order_count:
				order.status = "done" 
				order.save()
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
				).exclude(date__in=rest)
		return queryset
	def create(self, request, *args, **kwargs):
		ret = super(ScheduleList, self).create(request, args,kwargs)
		order = Order.objects.get(id=request.POST["order"])
		ordered_count = Schedule.objects.filter(order=request.POST["order"],deleted=False).count()
		order_count = order.product.amount
		if ordered_count == order_count:
			order.status = "inprogress" 
			order.save()
		return ret


class ScheduleBulkCreate(ListBulkCreateAPIView):
	def create(self, request):
		#delete old
		#order = request.args["order"]
		Schedule.objects.filter(order=order,done=False).delete()
		super(ScheduleBulkCreate, self)

class ScheduleForReadPagination(pagination.CursorPagination):
	ordering = 'date'

class ScheduleForRead(generics.ListAPIView):
	pagination_class = ScheduleForReadPagination
	serializer_class = ScheduleSerializer 
	def get_queryset(self):
		usr = get_object_or_404(User, name=self.kwargs.get("name"))
		startdate = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		enddate = startdate + datetime.timedelta(days=7)

		startdate_str = datetime.datetime.strftime(startdate,"%Y-%m-%d")
		enddate_str = datetime.datetime.strftime(enddate,"%Y-%m-%d")
		daterange = [startdate_str, enddate_str]

		if usr.iscoach:
			#queryset = Schedule.objects.filter(coach=usr.id,
			#		date__range=daterange).order_by('date','hour')
			queryset = Schedule.objects.filter(coach=usr.id, done=False)
			print queryset
		else:
			#queryset = Schedule.objects.filter(custom=usr.id,
			#		date__range=daterange).order_by('date','hour')
			queryset = Schedule.objects.filter(custom=usr.id, done=False)
			print queryset
		return queryset

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

		out = map(lambda x: int(x), outhours)
		ava = [h for h in range(0,26) if not h in out]
		print date
		print datetime.datetime.today()
		if (str((date.weekday() + 1)%7) in weekrest) or (date <= datetime.datetime.today()):
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

