from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
import json
from django.utils import timezone
from django.db.models import Sum
from rest_framework.pagination import PageNumberPagination 
from usr.models import *
from order.models import *
from business.models import *
from usr.serializers import *
from weibo.serializers import *
from business.serializers import *

import calendar
import pprint
import datetime 
import time



WEBVERSION = 1
MOBILEVERSION = 1
VERSION = 1

def add_months(sourcedate,months):
	month = sourcedate.month - 1 + months
	year = int(sourcedate.year + month / 12 )
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return datetime.date(year,month,day)

class CurrentVersionItem(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = CurrentVersionSerializer
        def get_object(self):
            version = 0
            if self.kwargs['client'] == "web":
                version = WEBVERSION
            if self.kwargs['client'] == "mobile":
                version = MOBILEVERSION
            ret, created = CurrentVersion.objects.get_or_create(name=self.kwargs['name'],client=self.kwargs['client'],version=version)
            if created:
                ret.version = 0
            return ret

class CoachStatistics(APIView):
        def get(self, request, name):
            usr = get_object_or_404(User,name=name)
            print usr
	    startday = datetime.datetime.strptime(request.GET['start'],"%Y%m%d").date()
	    endday = datetime.datetime.strptime(request.GET['end'],"%Y%m%d").date()
            #get all course
            courses = usr.sealed_time.filter(done=True,\
                    date__gt = startday,\
                    date__lt = endday)
            print courses.count()
            trial = 0
            normal = 0
            customers_set = []
            orders = []
            price = 0
            morethanonce = 0
            price_strict = 0
            order_strict = []
            #count trail
            for c in courses:
                if c.coursetype == "trial":
                    trial += 1
                else:
                    normal += 1
                if c.coursetype != "trial" and not c.custom in customers_set:
                    customers_set.append(c.custom)
                if not c.order is None and not c.order in orders:
                    orders.append(c.order)
                    price += c.order.amount
                    if c.order.coach == usr and not c.order in order_strict:
                        price_strict += c.order.amount
                        order_strict.append(c.order)
                        if not c.order.isfirst:
                            morethanonce += 1

                        

            return Response({"trial": trial, \
                    "price": price,\
                    "order": len(orders),\
                    "price_strict": price_strict,\
                    "order_strict": len(order_strict),\
                    "morethanonce": morethanonce, \
                    "customer": len(customers_set), \
                    "normal":normal})

class TrainSummary(APIView):
        def get(self, request, name):
            usr = get_object_or_404(User,name=name)
            all_done = usr.booked_time.filter(done=True).exclude(coursetype="trial").order_by("-date")
            # done count
            done_count = len(all_done)
            # last train
            last_train = -1
	    today = datetime.date.today()
            for item in all_done:
                last_train_date = item.date
                last_train = (today - last_train_date).days
                break
            # calculate rest
            coursecount = 0
            orders = Order.objects.filter(custom=usr)
            for order in orders:
                coursecount += order.product.amount

            # calculate avarage
            average = -1
            if done_count > 0:
                first_train = all_done.last()
                first_train_date = first_train.date
                endday = today
                if coursecount == done_count:
                    endday = all_done.first().date
                days = (today - first_train_date).days
                average = float(days)/float(done_count)
                average = int(10 * average)/float(10)

            #balance = Balance.objects.get(name=name,gym=int(gym))
            
            return Response({"done": done_count, \
                    "last_train":last_train, \
                    "average":average, \
                    "allcourse": coursecount, \
                    "rest": coursecount - done_count, \
                    #"balance": balance.balance, \
                    }, status=status.HTTP_200_OK)



class AllCourses(generics.ListAPIView):
    serializer_class = ScheduleSimpleSerializer
    pagination_class = None
    def get_queryset(self):
	usr = get_object_or_404(User, name=self.kwargs["name"])
        return usr.booked_time.order_by("date")

@api_view(['POST'])
def register(request):
	VALID_USER_FIELDS = [f.name for f in get_user_model()._meta.fields]
	DEFAULTS = {
			}
	serialized = UserRegisterationSerializer(data=request.data)
	if serialized.is_valid():
		user_data = {field: data for (field, data) in request.data.items() if field in VALID_USER_FIELDS}
		user_data.update(DEFAULTS)
		user = get_user_model().objects.create_user(
				**user_data
				)
		return Response(UserRegisterationSerializer(instance=user).data, status=status.HTTP_201_CREATED)
	else:
		return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

class UserList(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	def create(self, request, *args, **kwargs):
                if 'trial' in request.data:
                    #fix default name for trial
                    if request.data['name'] == "":
                        ts = int(time.time())
                        request.data['name'] = "0"+str(ts)

                    if User.objects.filter(name=request.data['name']):
                        usr =  User.objects.get(name=request.data["name"])
                        usr.trial = request.data['trial']
                        usr.created = timezone.now()
                        usr.save()

		resp = super(UserList, self).create(request, args, kwargs)

                if User.objects.filter(name=request.data['name']):
                        usr =  User.objects.get(name=request.data["name"])
                        usr.created = timezone.now()
                        usr.save()

		tl = TimeLine.objects.create(name=get_object_or_404(User, name=request.data["name"]))
		tl.followedby.add(tl)
		wh = WorkingDays.objects.create(name=request.data["name"])
                return resp
		#return Response({"result": 0})
		

class UserItemPatch(generics.GenericAPIView, UpdateModelMixin):
	lookup_field = "name"
	queryset = User.objects.all()
	serializer_class = UserSerializer
        def put(self, request, *args, **kwargs):
            return self.partial_update(request, *args, **kwargs)

        
class UserItem(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = "name"
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserItemByOpenId(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = "openid"
	queryset = User.objects.all()
	serializer_class = SimpleUserSerilaizer


class TimeLineList(generics.ListCreateAPIView):
	queryset = TimeLine.objects.all()
	serializer_class = TimeLineSerializer

class TimeLineItem(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = "name"
	serializer_class = TimeLineSerializer

	def get_queryset(self):
		obj = get_object_or_404(TimeLine,name=self.kwargs.get("name"))
		return TimeLine.objects.all()

class Following(generics.ListAPIView):
	lookup_field = "name"
	serializer_class = TimeLineSerializer
	pagination_class = None
	def get_queryset(self):
		return TimeLine.objects.get(name=self.kwargs.get('name')).follows.all()

class Feed(generics.ListAPIView):
	lookup_field = "name"
	serializer_class = ReadWeiboSerializer
	def get_queryset(self):
		#clean 
		if not "cursor" in self.request.query_params:
			TimeLine.objects.get(name=self.kwargs.get('name')).refresh.clear()
		return TimeLine.objects.get(name=self.kwargs.get('name')).feed.all()

class AlbumPagination(PageNumberPagination):       
           page_size = 100

class Album(generics.ListAPIView):
	lookup_field = "name"
	serializer_class = ImageSerializer 
        pagination_class = AlbumPagination
	def get_queryset(self):
		return User.objects.get(name=self.kwargs.get('name')).album.all().order_by("-created")

class AlbumUpdate(APIView):
	def post(self, request, name):
		usr = get_object_or_404(User, name=name)
		#usr.album.empty()
		print request(request.DATA["pics"])
		usr.ablum.add(request.DATA["pics"])
		return Response({"result":0}, status=status.HTTP_202_ACCEPTED)

class Courses(generics.ListAPIView):
	lookup_field = "name"
	serializer_class = CourseSerializer 
	def get_queryset(self):
		return User.objects.get(name=self.kwargs.get('name')).teaching.all()


class Refresh(generics.ListAPIView):
	lookup_field = "name"
	serializer_class = ReadWeiboSerializer
	#disable pagination
	pagination_class = None

	def get_queryset(self):
		return TimeLine.objects.get(name=self.kwargs.get('name')).refresh.all()

	def get(self, request, *args, **kwargs):
		resp = super(Refresh, self).get(request, args, kwargs)
		#delete refresh
		TimeLine.objects.get(name=self.kwargs.get('name')).refresh.clear()
		return resp


class Follow(APIView):
	def get(self, request, name, action):
		usr = get_object_or_404(TimeLine,name=name)
		tar = get_object_or_404(TimeLine,name=request.GET['target'])
		if action == 'follow':
			tar.followedby.add(usr)
			tar.save()
			return Response({'msg':'followed ' + str(tar.name)}, status=status.HTTP_202_ACCEPTED)
		else:
			tar.followedby.remove(usr)
			tar.save()
			return Response({'msg':'unfollowed ' + str(tar.name)}, status=status.HTTP_202_ACCEPTED)

class PersonUp(APIView):
	def get(self, request, by, personname, upaction):
		usr = get_object_or_404(User, name=by)
		person = get_object_or_404(User, name = personname)
		if upaction == 'up':
			if not usr.upped_person.filter(id=person.id).exists():
				usr.upped_person.add(person)
				person.upnum = person.upnum + 1
		else:
			if usr.upped_person.filter(id=person.id).exists():
				person.upped.remove(person)
				person.upnum = person.upnum - 1
		usr.save()
		person.save()
		serializer = UserSerializer(person)
		return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

class WorkingDaysView(APIView):
	def get(self, request, name):
		wd = get_object_or_404(WorkingDays, name=name)
		#filter all past date
		today = datetime.date.today()
		excep_work = filter(bool,wd.excep_work.split("|"))
		excep_rest = filter(bool,wd.excep_rest.split("|"))
		excep_work_filtered = [ a for a in excep_work if
				datetime.datetime.strptime(a,"%Y/%m/%d").date() > today]
		excep_rest_filtered = [ a for a in excep_rest if
				datetime.datetime.strptime(a,"%Y/%m/%d").date() > today]
		wd.excep_rest = "|".join(excep_rest_filtered)
		wd.excep_work = "|".join(excep_work_filtered)
		wd.save()
		serializer = WorkingDaysSerializer(wd)
		return Response(serializer.data, status=status.HTTP_200_OK)
	def patch(self, request, name):
		wd = get_object_or_404(WorkingDays, name=name)
		wd.weekrest = request.DATA["weekrest"]
		wd.excep_work = request.DATA["excep_work"]
		wd.excep_rest = request.DATA["excep_rest"]
		wd.out_hours = request.DATA["out_hours"]
		wd.noon_hours = request.DATA["noon_hours"]
		wd.save()
		serializer = WorkingDaysSerializer(wd)
		return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
class CoachComments(generics.ListAPIView): 
	serializer_class = ScheduleSerializer
	def get_queryset(self):
		usr = get_object_or_404(User, name=self.kwargs.get("name"))
		return usr.sealed_time.exclude(rate__isnull=True)

class RespCustomerList(generics.ListAPIView):
	serializer_class = SimpleUserWithLastDateSerilaizer
	pagination_class = None
	def get_queryset(self):
		ret = User.objects.filter(owner = self.kwargs['name'], order_status__in = ['paid','inprogress'])
                for i in ret:
                    i.update_owner_status()
		ret = User.objects.filter(owner = self.kwargs['name'], order_status__in = ['paid','inprogress'])
                return ret


class CustomerList(generics.ListAPIView):
	serializer_class = SimpleUserSerilaizer
	pagination_class = None
	def get_queryset(self):
		usr = get_object_or_404(User, name=self.kwargs["name"])
		#customers =  usr.sealed_time.values_list("custom",flat=True)
		gym =  usr.gym.first()
		#print customers
		customlist = gym.get_all_customers()
                triallist= list(set(User.objects.filter(trial=gym.id).values_list('name', flat=True)))

                customlist = list(set(customlist + triallist))


		end = datetime.datetime.now() + datetime.timedelta(days=-7)
		ret = User.objects.filter(name__in = customlist).exclude(trial=gym.id,created__lt=end)

		if ret.count() == 0:
			ret = User.objects.filter(name = usr.name)

                for c in ret:
                    if c.owner is None:
                        c.find_owner()
                    if c.order_status is None:
                        c.update_owner_status()
		return ret


class ModifyGym(APIView):
	def post(self, request, name):
		usr = get_object_or_404(User, name=self.kwargs["name"])
		if "gym" in request.data:
			newgym = get_object_or_404(Gym,id=request.data['gym'])
			usr.gym = [newgym]

			#BUG: where creating new coach, the field iscoach is false
			#set to coach when set gym    
			#now when creating new coach there is 2 step: 1.create a new user 2.change the gym
			usr.iscoach = True

			usr.save()
			serializer = GymSerializer(newgym)
			return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
		else:
			usr.gym = []
			usr.save()
			return Response({"msg":"empty gym"}, status=status.HTTP_202_ACCEPTED)


class InCome(APIView):
	def cal_course_income(self,query):
		price = 0
		for course in query:
			price += course.getprice()
		return price
	def get(self, request, name):
		usr = get_object_or_404(User, name=name)
		if "end" in request.GET:
			end = datetime.datetime.strptime(request.GET["end"], "%Y%m%d")
		else:
			end = datetime.date.today()

		if "start" in request.GET:
			start = datetime.datetime.strptime(request.GET["start"], "%Y%m%d")
		else:
			start = add_months(end, -1)
		#end = end + datetime.timedelta(days=1)
		print start
		print end + datetime.timedelta(hours=24)
		orders = usr.income_orders.filter(paidtime__range=[start,end+datetime.timedelta(hours=24)])

		sold = 0
		sold_count = 0
		for order in orders:
			sold += order.amount
			sold_count += order.product.amount

		sold_xu = orders.filter(isfirst=False).aggregate(Sum('amount'))["amount__sum"] or 0

		courses = usr.sealed_time.filter(date__range=[start,end],done=True).exclude(coursetype ='trial')

		exp_courses = usr.sealed_time.filter(date__range=[start,end],done=True, order=None,coursetype="trial")


                #groupcourse_person = 
                group_courses = GroupCourseInstanceBook.objects.filter(date__range=[start,end], coach = usr.name)
                for c in group_courses:
                    c.update_coach()
                
		#courses = orders.value_list("schedule")
		return Response({"sold_xu":sold_xu,\
                    "sold_price": sold, \
                    "sold_count": sold_count, \
                    "completed_course":courses.count() or 0, \
                    "completed_course_price":self.cal_course_income(courses), \
                    "exp_courses": exp_courses.count(), \
                    "group_courses": group_courses.count()})


class FeedbackList(generics.ListCreateAPIView):
	queryset = FeedBack.objects.all()
	serializer_class = FeedBackSerializer 


class ChargeHistoryList(generics.ListCreateAPIView):
        serializer_class = ChargeHistorySerializer
        def get_queryset(self):
	    return ChargeHistory.objects.all().filter(name=self.kwargs['name'])

	def create(self, request, *args, **kwargs):
            #...
	    resp = super(ChargeHistoryList, self).create(request, args, kwargs)
            #chage  to user
            balance,_ = Balance.objects.get_or_create(name=kwargs['name'], gym=int(kwargs['gym']))
            balance.charge(request.data['amount'])
            return resp

class MessageList(generics.ListCreateAPIView):
        pagination_class = None
	serializer_class = MessageSerializer
	def get_queryset(self):
	    return Message.objects.all().filter(done=False,name=self.kwargs["name"])

class MessageItem(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = "id"
        queryset = Message.objects.all().filter(done=False)
	serializer_class = MessageSerializer

class ThresholdMsgList(generics.ListCreateAPIView):
        pagination_class = None
	serializer_class = ThresholdMsgSerializer
	def get_queryset(self):
	    return ThresholdMsg.objects.all().filter(name=self.kwargs["name"]).exclude(status="dismissed")

class ThresholdMsgItem(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = "id"
	serializer_class = ThresholdMsgSerializer 
        queryset = ThresholdMsg.objects.all()

	def partial_update(self, request, *args, **kwargs):
		ret = super(ThresholdMsgItem, self).partial_update(request, args,kwargs)
                if request.data['status'] == 'sent':
                    self.get_object().send_msg()
                return ret

class TagQueryList(generics.ListCreateAPIView):
	serializer_class = TagIndexSerializer
        pagination_class = None
	def get_queryset(self):
            return TagIndex.objects.all().filter(gym=self.kwargs['gymid'],tag=self.request.GET['tag'])

