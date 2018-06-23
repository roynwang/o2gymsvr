# coding=utf-8
from django.shortcuts import render
from django.db.models import Count
from business.models import *
from business.serializers import *
from order.models import *
from usr.models import *
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet
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
import pprint
from django.http import JsonResponse
from traincategory.models import *
from rest_framework.exceptions import NotAcceptable
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class ChargePricingList(generics.ListAPIView):
	serializer_class = ChargePricingSerializer
	pagination_class = None

        def get_queryset(self):
            gym = self.kwargs.get("pk")
            return ChargePricing.objects.filter(gym=gym)

class ReimbursementList(generics.ListAPIView):
	serializer_class = FinanceSerializer
	pagination_class = None

        def get_queryset(self):
            name = self.kwargs.get("name")
            usr = get_object_or_404(User, name=name)
            return Finance.objects.filter(by=usr.displayname).order_by("-date").limit(30)

class FinanceList(generics.ListCreateAPIView):
	serializer_class = FinanceSerializer
	pagination_class = None


        def archieve(self,gym, start,end):
            #archieve order
            gyminst = Gym.objects.get(id=gym)
            orders = Order.objects.filter(gym=gyminst, paidtime__range=[start,end])
            result = {}
            for order in orders:
                    datestr = datetime.datetime.strftime(order.paidtime.date(), "%Y%m%d")
                    if not datestr in result:
                        result[datestr] = 0
                    result[datestr] += order.amount
                
            #archieve balance order
            borders = BalanceOrder.objects.filter(gym=gym,status="completed",updated__range=[start,end])
            for border in borders:
                    datestr = datetime.datetime.strftime(border.updated.date(), "%Y%m%d")
                    if not datestr in result:
                        result[datestr] = 0
                    result[datestr] += border.paid_amount

            for tmp in result:
                d = datetime.datetime.strptime(tmp,"%Y%m%d").date()
                if Finance.objects.filter(date=d, gym=gym,cate='收入').count() != 0:
                    continue
                Finance.objects.create(gym=gym, \
                        date = d,
                        brief = '收入',
                        by = 'system',
                        op = 'system',
                        cate = '收入',
                        amount = result[tmp],
                        channel = '其他',
                        memo = 'auto archieve')

        def get_queryset(self):
            #1 get date range
            startdate = self.request.GET["start"]
            enddate = self.request.GET["end"]
            pk = self.kwargs.get("pk")


            startday = datetime.datetime.strptime(startdate,"%Y%m%d")
            endday = datetime.datetime.strptime(enddate,"%Y%m%d")
            #archieve
            
            allitems = Finance.objects.filter(gym=int(pk), date__range=[ startday,endday]).order_by("-date")

            self.archieve(int(pk),startday,endday)
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

class ScheduleDetailItem(generics.RetrieveUpdateAPIView):
	serializer_class = ScheduleSerializer
        lookup_field = "pk"
        queryset = Schedule.objects.all()

class ScheduleDetailItemPatch(generics.GenericAPIView, UpdateModelMixin):
	serializer_class = ScheduleSerializer
        lookup_field = "pk"
        queryset = Schedule.objects.all()
        def put(self, request, *args, **kwargs):
	    ret = self.partial_update(request, args,kwargs)
            if "detail" in request.data and request.data["detail"] != "":
                course = self.get_object()
                cache.set("o2_coachaction_" + course.coach.name, request.data["detail"], None)
                actions = json.loads(request.data["detail"])
                cache.delete("o2_detailcache_" + course.custom.name)
                for item in actions:
                    if item["contenttype"] == "action":
                        CustomerWorkoutValue.objects.update_or_create(customer=course.custom.name,\
                            name=item['name'], \
                            workoutid=item['workoutid'], \
                            defaults={"unit":item["unit"],"weight":item['weight'],"repeattimes":item['repeattimes'], \
                            "comments":item['comments']})
            return ret


class ScheduleComplete(generics.RetrieveAPIView):
        serializer_class = ScheduleSerializer
        def get_object(self):
            sid = self.kwargs.get("pk")
            s = get_object_or_404(Schedule, id=sid)
            s.user_confirm()
            return s

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
        def destroy(self, request, *args, **kwargs):
                schedule = self.get_object()
                if schedule.coursetype == "charge":
                    gym = schedule.coach.get_coach_gym()
                    balance = Balance.objects.get(gym=gym.id, name=schedule.custom.name)
                    balance.cancelconsume(schedule.price - schedule.discount)
                

                #2 get all schedule
                if schedule.detail != "[]":
                    print schedule.detail
                    cache.set("o2_detailcache_" + schedule.custom.name, schedule.detail, None)
                
		return super(ScheduleItem, self).destroy(request, args,kwargs)

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

                
                if ("done" in request.data and request.data["done"]) or "order" in request.data:
                        self.get_object().doneBook()
                        self.get_object().create_threshold_msg()

                if "detail" in request.data and request.data["detail"] != "":
                    course = self.get_object()
                    #remove cache
                    cache.set("o2_coachaction_" + course.coach.name, request.data["detail"], None)
                    actions = json.loads(request.data["detail"])
                    cache.delete("o2_detailcache_" + course.custom.name)

                    for item in actions:
                        if item["contenttype"] == "action":
                            CustomerWorkoutValue.objects.update_or_create(customer=course.custom.name,\
                                    name=item['name'], \
                                    workoutid=item['workoutid'], \
                                    defaults={"unit":item["unit"],"weight":item['weight'],"repeattimes":item['repeattimes'], \
                                    "comments":item['comments']})
		return ret

class GymScheduleList(generics.ListAPIView):
	pagination_class = None
	serializer_class = ScheduleSerializer 
	def get_queryset(self):
		gym = get_object_or_404(Gym, id=self.kwargs.get("pk"))
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		queryset = Schedule.objects.filter(coach__in=gym.coaches.values_list("id",flat=True), date=date).order_by("hour")
		return queryset

class SelfTrainList(generics.ListCreateAPIView):
	serializer_class = SelfTrainSerializer
	pagination_class = None

        def get_queryset(self):
            startdate = datetime.datetime.strptime(self.request.GET["start"],"%Y%m%d")
	    enddate = datetime.datetime.strptime(self.request.GET["end"],"%Y%m%d")
	    daterange = [startdate, enddate]
	    queryset = SelfTrain.objects.filter(gym=self.kwargs.get("pk"),date__range=daterange).order_by("date","hour")
            return queryset


class SelfTrainByDateList(generics.ListAPIView):
	pagination_class = None
	serializer_class = SelfTrainSerializer
        def get_queryset(self):
	    pk=self.kwargs.get("pk")
	    date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
	    queryset = SelfTrain.objects.filter(gym=pk, date=date)
            return queryset


class SelfTrainItem(generics.RetrieveDestroyAPIView):
	serializer_class = SelfTrainSerializer
        lookup_field = "pk"
        queryset = SelfTrain.objects.all()

class ScheduleSurvey(APIView):
        def get(self, request, courseid):
            course = Schedule.objects.get(id=int(courseid))
            mdetail = course.create_newcustomer_survey()
            if not mdetail is False:
                return Response(mdetail, status=status.HTTP_200_OK)
            return Response({}, status=status.HTTP_200_OK)

        def post(self, request, courseid):
            course = Schedule.objects.get(id=int(courseid))
            customer = course.custom
            coach = course.coach

            user = customer
            print request.data
            for k in request.data:
                Survey.objects.create( \
                        courseid = int(courseid), \
                        score = k["score"], \
                        date = course.date, \
                        coach = coach.name, \
                        customer = customer.name, \
                        question = k["question"])
            return Response({}, status=status.HTTP_200_OK)

class CurrentCoach(APIView):
        def get(self, request, name):
            usr = get_object_or_404(User, name = name)
            course = usr.booked_time.order_by("-date")
            coachname = ""
            if course.count() != 0:
                coachname = course[0].coach.name
            return Response({"coach":coachname}, status=status.HTTP_200_OK)

class TargetView(APIView):
        def get(self, request,name):
            ret = { "done_count": 0,\
                    "before_day": 0,\
                    "before_trainning": 0,\
                    "diet_score": 0, \
                    "train_score": 0 }

            usr = get_object_or_404(User, name=name)
	    today = datetime.datetime.today()
            ret['done_count'] = usr.booked_time.filter(done=True).count()
            ret['before_day'], ret['before_trainning'] = usr.get_to_next_eval()
            kpi = CustomerWeeklyKPI.objects.filter(customer=usr.name, archived=True) \
                    .order_by("-date").first()
            pprint.pprint(kpi.diet_score)

            ret['diet_score'] =  kpi.diet_score
            ret['train_score'] =  kpi.train_score

            return Response(ret, status=status.HTTP_200_OK)


class GymLoadList(APIView):
        def get(self, request, pk, date):
	    gym = get_object_or_404(Gym, id=self.kwargs.get("pk"))
	    date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
	    queryset = Schedule.objects.filter(coach__in=gym.coaches.values_list("id",flat=True), date=date).order_by("hour")
            #init
            ret = []
            for i in range(0,26):
                ret.append({'hour':i,'course_count':0, 'available': 1,'selftrain':0})

            for p in queryset:
                ret[p.hour]['course_count'] += 1
                ret[p.hour+1]['course_count'] += 1

            selftrain = SelfTrain.objects.filter(gym=self.kwargs.get("pk"), date=date)
            for hour in selftrain:
                ret[hour.hour]['course_count'] += 1
                if 'name' in self.request.GET:
                    name = self.request.GET['name']
                    if name == hour.name:
                        ret[hour.hour]['selftrain'] = hour.id
                        ret[hour.hour]['available'] = 2

            for item in ret:
                if item['course_count'] >= 4 or item['selftrain']:
                    if item['available'] == 1:
                        item['available'] = 0

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
                coursetype = "trial"
                price = 0
                discount_amount = 0

                if "order" in request.data:
         	        order = Order.objects.get(id=request.data["order"])
                        coursetype = "normal"

                if "coursetype" in request.data and request.data['coursetype'] == "charge":
                        coursetype = "charge"
                        price  = 350
			day = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d").date()
                        _,discount = get_discount(customer.name, day)
                        amount = price - int(price*discount/100)
                        discount_amount = int(price*discount/100)
                        gym = coach.get_coach_gym()
                        balance = Balance.objects.get(name=customer.name,gym=gym.id)
                        if balance.precheck(amount):
                            balance.consume(amount)
                        else:
                            raise NotAcceptable('infficient balance')

                detail = "[]"
                mkey = "o2_detailcache_" + customer.name
                mdetail = cache.get(mkey)
                print mdetail
                print "xxxxxxxxxxxx"
                if not mdetail is None:
                    detail = mdetail

		book = Schedule.objects.create(coach=coach,
				custom=customer,
				date= datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d").date(),
				hour=request.data["hour"],
				order=order,
                                coursetype=coursetype,
                                price=price,
                                discount=discount_amount,
                                detail=detail)
		if "done" in request.data:
			book.done = request.data["done"]
			book.save()


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
                #book.send_launch_notification()
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
		if usr.iscoach:
	    	    return usr.sealed_time.filter(date__range=daterange).order_by("date","hour")
	    	return usr.booked_time.filter(date__range=daterange).order_by("date","hour")

class CoachTodayKPI(APIView):
        def getkpi(self,enddate,queryset):
                customers = []
                customercount = 0
                coursecount = 0
                floor = enddate - datetime.timedelta(days=30)
                ceil = enddate.date()
                
                for item in queryset:
                    if item.date > ceil or item.date <= floor.date():
                        continue
                    coursecount += 1
                    if not item.custom in customers:
                        customers.append(item.custom)
                daterange = [floor, ceil]
                allcourses = Schedule.objects.filter(custom__in=customers,\
                        date__range=daterange,coursetype__in=["normal","charge"], done=True)
                coursecount = allcourses.count()

                return {"day": datetime.date.strftime(enddate, "%Y%m%d"), \
                        "customercount":len(customers),\
                        "average": float(coursecount)/len(customers),\
                        "coursecount": coursecount}

	def get(self, request, name):
		usr = get_object_or_404(User, name=name)
	        oristartdate = datetime.datetime.today() - datetime.timedelta(days=30)
	        startdate = oristartdate - datetime.timedelta(days=30)
	        enddate = datetime.datetime.today()
		daterange = [startdate, enddate]

	    	q = usr.sealed_time.filter(date__range=daterange,coursetype__in=["normal","charge"]).order_by("date","hour")
                ret = []
                d = oristartdate
                while d < enddate:
                    ret.append(self.getkpi(d,q))
                    d = d + datetime.timedelta(days=1)
       
                maxaverage = 0
                for item in ret:
                    if maxaverage < item['average']:
                        maxaverage = item['average']
                lastday = ret[-1]
                pprint.pprint(ret);
                return Response({"month":"{:1.2f}".format(maxaverage*0.95), "today":"{:1.2f}".format(lastday['average'])})

class CustomerKPIDetailView(APIView):
    def get(self, request, name):
	    usr = get_object_or_404(User, name=name)
	    ori_date = datetime.datetime.strptime(self.request.GET["date"],"%Y%m%d")
            delta = range(1,8)[ori_date.weekday()]

            enddate = ori_date - datetime.timedelta(days=delta)
            startdate = enddate - datetime.timedelta(days=7)

            schedules = usr.sealed_time.filter(date__range=[startdate.date(), enddate.date()], \
                    done=True,coursetype__in=['normal','charge'])
            schedules_count = schedules.count()
            customer_group = schedules.values('custom__displayname','custom__name').annotate(total=Count('id'))

            archived = CustomerWeeklyKPI.objects.filter(coach=usr.name,date=enddate)
            if archived.filter(archived=True).count() <= len(customer_group):
                is_end = False
                if enddate < datetime.datetime.today():
                    is_end = True
                for item in customer_group:
                    if archived.filter(archived=True,\
                        customer=item['custom__name'], date=enddate) \
                        .count() == 0 :
                            custom = get_object_or_404(User,name=item['custom__name'])
                            actual_times = Schedule.objects.filter(custom=custom, \
                                    date__range=[startdate.date(), enddate.date()], \
                                    done = True,
                                    coursetype__in=['normal','charge']).count()
                            CustomerWeeklyKPI.objects.update_or_create(\
                                    customer=item['custom__name'],\
                                    date=enddate,\
                                    defaults={"archived":is_end, 'actual_times':actual_times, 'coach':usr.name})

            
            queryset = archived.filter(coach=usr.name, date=enddate)
            serializer = CustomerWeeklyKPISerializer(queryset, many=True)

            startdatestr = datetime.date.strftime(startdate, "%m/%d")
            enddatestr = datetime.date.strftime(enddate, "%m/%d")
            return Response({'startdate':startdatestr, 'enddate':enddatestr, 'customers':serializer.data})

class CustomerWeeklyKPIItemView(generics.RetrieveUpdateAPIView):
	serializer_class = CustomerWeeklyKPISerializer

	def get_object(self):
	    obj = get_object_or_404(CustomerWeeklyKPI, \
                    customer=self.kwargs.get("name"), \
                    date=self.kwargs.get("date"))
            return obj

	def partial_update(self, request, *args, **kwargs):
            obj, created = CustomerWeeklyKPI.objects.get_or_create(customer=kwargs["name"], date=kwargs["date"])
	    date = datetime.datetime.strptime(kwargs["date"],"%Y-%m-%d")
            if date <= datetime.datetime.today():
                obj.archived = True
                obj.save()
	    ret = super(CustomerWeeklyKPIItemView, self).partial_update(request, args,kwargs)
            return ret

class CoachKPI(APIView):
        def getkpi(self,enddate,queryset):
                customers = []
                customercount = 0
                coursecount = 0
                floor = enddate - datetime.timedelta(days=30)
                ceil = enddate.date()
                
                for item in queryset:
                    if item.date > ceil or item.date <= floor.date():
                        continue
                    coursecount += 1
                    if not item.custom in customers:
                        customers.append(item.custom)
                daterange = [floor, ceil]
                allcourses = Schedule.objects.filter(custom__in=customers,\
                        date__range=daterange,coursetype__in=["normal","charge"], done=True)
                coursecount = allcourses.count()

                return {"day": datetime.date.strftime(enddate, "%Y%m%d"), \
                        "customercount":len(customers),\
                        "average": float(coursecount)/len(customers),\
                        "coursecount": coursecount}

	def get(self, request, name):
		usr = get_object_or_404(User, name=name)
	        oristartdate = datetime.datetime.strptime(self.request.GET["start"],"%Y%m%d")
	        startdate = oristartdate - datetime.timedelta(days=30)
	        enddate = datetime.datetime.strptime(self.request.GET["end"],"%Y%m%d")
		daterange = [startdate, enddate]
	    	q = usr.sealed_time.filter(date__range=daterange,coursetype__in=["normal","charge"]).order_by("date","hour")
                ret = []
                d = oristartdate
                while d < enddate:
                    ret.append(self.getkpi(d,q))
                    d = d + datetime.timedelta(days=1)
                return Response(ret)

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
            allschedule = Schedule.objects.filter(coach__in=gym.coaches.values_list("id",flat=True),done=True,date__range=[startday, endday]).exclude(coursetype = 'trial')
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

class BodyEvalDataView(generics.ListAPIView):
	pagination_class = None
	serializer_class = BodyEvalSerializer
	def get_queryset(self):
		return BodyEval.objects.filter(name=self.kwargs.get("name")) \
                        .exclude(group__in=["4.背面观","5.侧面观","3.正面观"]) \
                        .order_by("date")



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
		ret = Schedule.objects.filter(date__lt=today,done=False,order__in=orders).order_by("date","hour")
		return ret

		
		
class GymSumSale(APIView):	
	def get(self,request,pk):
                mkey = "o2_salesum_" + str(pk)
                mdetail = cache.get(mkey)
                if mdetail:
                    return Response(mdetail)
		gym = get_object_or_404(Gym, id=pk)
		sum_coursecount = 0
                sum_completedcount = 0
                sum_expiredcount = 0
                today = datetime.datetime.strftime(datetime.datetime.today(),"%Y-%m-%d")
		for o in gym.orders.iterator():
                        a = o.product.amount
			sum_coursecount += o.product.amount
                        c = o.schedule_set.count()
                        sum_completedcount += o.schedule_set.count()
                        endtime = o.cal_endtime()
                        if endtime != "N/A" and endtime < today:
                            sum_expiredcount += (a - c)
                result ={"sum_expiredcount": sum_expiredcount, "sum_coursecount":sum_coursecount, "sum_completedcount": sum_completedcount}
                mdetail = cache.set(mkey, result, 60*60*24)
                return Response(result)
		


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

@csrf_exempt
def show_complete_survey_group(request, courseid):
        course = GroupCourseInstance.objects.get(id=int(courseid))
        coach = get_object_or_404(User, name=course.coach)
        course_detail = GroupCourse.objects.get(id=course.course)

        questions = [ \
                '我在训练中感受到了充分的鼓励', \
                '我能理解并学会教练讲授的动作要领', \
                '我觉得训练强度合理']
        for i in [1,2,3,]:
            k = 'q' + str(i)
            if k in request.POST:
                Survey.objects.create( \
                        courseid = int(courseid), \
                        score = request.POST[k], \
                        date = course.date, \
                        coach = coach.name, \
                        customer = "", \
                        course_type = "group", \
                        question = questions[i-1])

        ret = render(request, "postsurvey/complete.html",{})
        return ret


@csrf_exempt
def show_complete_survey(request, courseid):
        course = Schedule.objects.get(id=int(courseid))
        customer = course.custom
        coach = course.coach

        user = customer
        startday = datetime.datetime.today() + datetime.timedelta(days=-30)
        times = user.booked_time.filter(date__gt=startday).count()

        questions = [ \
                '现在课程的时间安排符合我的需求', \
                '我觉得课程内容和强度合理，对我很有帮助', \
                '教练能精力充沛的带我完成训练', \
                '教练总是在管理饮食上提供建议和帮助', \
                '教练会及时提醒并鼓励我来锻炼'
        ]
        for i in [1,2,3,4,5]:
            k = 'q' + str(i)
            if k in request.POST:
                Survey.objects.create( \
                        courseid = int(courseid), \
                        score = request.POST[k], \
                        date = course.date, \
                        coach = coach.name, \
                        customer = customer.name, \
                        question = questions[i-1])

        ret = render(request, "postsurvey/complete.html",\
                {"times":times, "questions":questions, "course":course,"customer":customer, "coach":coach})
        return ret

def show_post_survey_group(request, courseid):
        course = GroupCourseInstance.objects.get(id=int(courseid))
        course_detail = GroupCourse.objects.get(id=course.course)
        coach = get_object_or_404(User, name=course.coach)

        questions = [ \
                '我在训练中感受到了充分的鼓励', \
                '我能理解并学会教练讲授的动作要领', \
                '我觉得训练强度合理']

        template = "postsurvey/gsreport.html"
        '''
        if Survey.objects.filter(courseid = course.id).count() > 0:
            template = "postsurvey/complete.html"
        '''
        ret = render(request, template,\
                {"coursedetail":course_detail,"questions":questions, "course":course,"coach":coach})
        return ret



def show_post_survey(request, courseid):
        course = Schedule.objects.get(id=int(courseid))
        customer = course.custom
        coach = course.coach

        user = customer
        startday = datetime.datetime.today() + datetime.timedelta(days=-30)
        times = user.booked_time.filter(date__gt=startday).count()

        questions = [ \
                '现在课程的时间安排符合我的需求', \
                '我觉得课程内容和强度合理，对我很有帮助', \
                '教练能精力充沛的带我完成训练', \
                '教练总是在管理饮食上提供建议和帮助', \
                '教练会及时提醒并鼓励我来锻炼'
        ]

        template = "postsurvey/report.html"
        if Survey.objects.filter(courseid = course.id).count() > 0:
            template = "postsurvey/complete.html"
        ret = render(request, template,\
                {"times":times, "questions":questions, "course":course,"customer":customer, "coach":coach})
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
		ret = GroupCourseInstanceBook.objects.filter(customer=self.kwargs.get("name")).order_by("date").order_by("date")
		return ret

#TODO
class GymGroupCourseDayList(generics.ListCreateAPIView):
	serializer_class = GroupCourseInstanceSerializer
	pagination_class = None
	def get_queryset(self):
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
		ret = GroupCourseInstance.objects.filter(gym=self.kwargs.get("pk"),date=date.date())
		return ret

class GymGroupCourseWeekList(generics.ListAPIView):
	serializer_class = GroupCourseInstanceSerializer
	pagination_class = None
	def get_queryset(self):
		start_date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
                end_date = start_date + datetime.timedelta( days = 7)
		ret = GroupCourseInstance.objects.filter(gym=self.kwargs.get("pk"),
                        date__range=[start_date.date(), end_date.date()])
                print ret.query
		return ret


class GymSurveyList(generics.ListCreateAPIView):
	serializer_class = SurveySerializer
        pagination_class = None
        queryset = Survey.objects.all().order_by("-date")



class GymTodoList(generics.ListCreateAPIView):
	serializer_class = TodoSerializer
        pagination_class = None
	def get_queryset(self):
            date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")
	    pending = Todo.objects.filter(gym=self.kwargs.get("pk"), done = False, schedule_date__lt=date.date())
	    tody = Todo.objects.filter(gym=self.kwargs.get("pk"), schedule_date=date.date())
            return pending | tody

class RecurTodoView(APIView):
        def post(self, request, pk):
            item = Todo.objects.get(id=pk)
            times = int(request.data['times'])
            interval = int(request.data['interval'])
            for i in range(1, times):
                newday = item.schedule_date + datetime.timedelta( days = i*interval)
                Todo.objects.create(schedule_date = newday, \
                        by = item.by, \
                        gym = item.gym, \
                        content = item.content)
            return Response({}, status=status.HTTP_200_OK)
            

class TodoItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = Todo.objects.all()
        lookup_field = "pk"
	serializer_class = TodoSerializer


class GroupCourseItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = GroupCourse.objects.all()
	serializer_class = GroupCourseSerializer


class GroupCourseBookItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = GroupCourseInstanceBook.objects.all()
	serializer_class = GroupCourseInstanceBookSerializer
            
        '''
	def destroy(self, request, *args, **kwargs):
                book = GroupCourseInstanceBook.objects.get(id=self.kwargs.get("pk"))
                balance,_ =  Balance.objects.get_or_create(name=book.customer,gym=book.gym)
                balance.cancelconsume(book.price)
                balance.cancelconsume_groupcourse()
	        ret = super(GroupCourseBookItem, self).destroy(request, args,kwargs)
                return ret
        '''


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

        def create_first_time(self, request, *args, **kwargs):
                #get or create user
                phone = request.data['phone']
                if User.objects.filter(name=phone).exists():
                    customer = User.objects.get(name=phone)
                else:
                    sex = False
                    displayname = request.data['displayname']
                    if request.data["sex"] == '1':
        		sex = True
                 	customer = User.objects.create(name=phone,displayname=displayname,sex=sex,iscoach=False,created=datetime.datetime.now())
                    #bind open id to the user
                customer.openid = request.data['openid']
                customer.save()
                #create an book
                gc = GroupCourseInstanceBook.objects.create(customer=phone,\
                        course = request.data['course'],\
                        date = request.data['date'],\
                        gym = request.data['gym'],\
                        coach = request.data['coach'],\
                        price = 0)
                serializer = GroupCourseInstanceBookDetailSerializer(gc)
                return Response(serializer.data)

	def create(self, request, *args, **kwargs):
                #get course coach
                course = GroupCourseInstance.objects.get(id=request.data['course'])
                request.data['coach'] = course.coach

                if "firsttime" in request.data:
                    return self.create_first_time(request, args, kwargs)
                    
                #calculate dispcount
		date = datetime.datetime.strptime(self.kwargs.get("date"),"%Y%m%d")


                #get balance
                b = Balance.objects.get(name=request.data['customer'],gym=course.gym)
                if b.group_enddate and b.group_enddate>=date.date():
                    request.data['price'] = 0
		    ret = super(GymGroupCourseDayBookList, self).create(request, args,kwargs)
                    return ret
                if b.groupcourse_count > 0:
                    b.consume_groupcourse()
                    request.data['price'] = 0
                    request.data['groupcourse_price'] = 1
		    ret = super(GymGroupCourseDayBookList, self).create(request, args,kwargs)
                    return ret
                    

                _, discount = get_discount(request.data['customer'], date.date())

                gc = GroupCourseInstance.objects.get(id=request.data['course'])
                amount = gc.price - (gc.price * discount / 100)

                balance = Balance.objects.get(name=request.data['customer'],gym=int(request.data["gym"]))
                if not balance.precheck(amount):
                    raise NotAcceptable('infficient balance')
                balance.consume(amount)
                request.data['price'] = amount
		ret = super(GymGroupCourseDayBookList, self).create(request, args,kwargs)
                #consume balance
                return ret
                #create consumption log
class UserDateDiscountView(APIView):
        def get(self, request, name, date):
		date = datetime.datetime.strptime(date,"%Y%m%d")
                dura, discount = get_discount(name,date.date())
                b =  Balance.objects.get(name=name,gym=31)
                return Response({"dura":dura,"discount":discount,"enddate":b.group_enddate},status.HTTP_200_OK)


class UserSummaryView(APIView):
        def get(self, request, name, gym):
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

            balance,_ = Balance.objects.get_or_create(name=usr.name,gym=int(gym))
            order_count = Order.objects.filter(custom=usr.name).count()

            ret = {"name":usr.name,\
                    "displayname":usr.displayname,\
                    "balance":balance.balance,\
                    "groupcourse_balance":balance.groupcourse_count,\
                    "group_enddate": balance.group_enddate, \
                    "pt_count":pt_count,\
                    "gc_count":gc_count,\
                    "week_trained":week_trained,\
                    "discount": 0,\
                    "order_count":order_count}
            #get
            return Response(ret, status=status.HTTP_200_OK)


def get_before_date_last_trained(name,day):
            usr = get_object_or_404(User, name=name)
            last_pt = None
            if Schedule.objects.filter(date__lt=day, custom=usr).order_by("-date").count() >0 :
                last_pt = Schedule.objects.filter(date__lt=day, custom=usr).order_by("-date")[0].date

            last_gc = None
            last_gc_query = GroupCourseInstanceBook.objects \
                    .filter(customer=name,date__lte=datetime.datetime.today()) \
                    .order_by("-date")
            if last_gc_query.count() > 0:
                last_gc = last_gc_query[0].date

            last_trained_date = last_pt
            
            if last_trained_date is None:
                last_trained_date = last_gc

            if last_trained_date is None:
                return None

            if not last_gc is None and last_trained_date < last_gc:
                last_trained_date = last_gc
            return last_trained_date


def get_last_trained(name):
            usr = get_object_or_404(User, name=name)

            today = datetime.datetime.today()
            last_pt = None
            if Schedule.objects.filter(custom=usr,done=True).order_by("-date").count() >0 :
                last_pt = Schedule.objects.filter(custom=usr,done=True).order_by("-date")[0].date

            last_gc = None
            last_gc_query = GroupCourseInstanceBook.objects \
                    .filter(customer=name,date__lte=datetime.datetime.today()) \
                    .order_by("-date")
            if last_gc_query.count() > 0:
                last_gc = last_gc_query[0].date

            last_trained_date = last_pt
            
            if last_trained_date is None:
                last_trained_date = last_gc

            if last_trained_date is None:
                return None

            if not last_gc is None and last_trained_date < last_gc:
                last_trained_date = last_gc
            return last_trained_date


def get_discount(name, coursedate):
            last_trained_date = get_before_date_last_trained(name,coursedate)
            if last_trained_date is None:
                return (0,10)
            dura = (coursedate - last_trained_date).days
            if dura <= 3:
                return (dura,20)
            if dura <= 4:
                return (dura,10)
            return (0,0)
            #get groupcourse count
            '''
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
            '''
            return 0

            
class HomeworkListView(generics.ListCreateAPIView):
	serializer_class = HomeworkSerializer 
	pagination_class = None

        def get_queryset(self):
            customer = self.kwargs.get("name")
            return Homework.objects.filter(customer=customer)

        '''
	def create(self, request, *args, **kwargs):
            print request.data
        '''

class HomeworkItemView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Homework.objects.all()
	serializer_class = HomeworkSerializer 

class FinanceItemView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Finance.objects.all()
	serializer_class = FinanceSerializer

