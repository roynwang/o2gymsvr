from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
import json

from usr.models import *
from order.models import *
from usr.serializers import *
from weibo.serializers import *
from business.serializers import *

import pprint
import datetime

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
		resp = super(UserList, self).create(request, args, kwargs)

		tl = TimeLine.objects.create(name=get_object_or_404(User, name=request.data["name"]))
		tl.followedby.add(tl)
		wh = WorkingDays.objects.create(name=request.data["name"])

		return Response({"result": 0})

class UserItem(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = "name"
	queryset = User.objects.all()
	serializer_class = UserSerializer

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

class Album(generics.ListAPIView):
	lookup_field = "name"
	serializer_class = ImageSerializer 
	page_size = 20
	def get_queryset(self):
		return User.objects.get(name=self.kwargs.get('name')).album.all()
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

class CustomerList(generics.ListAPIView):
	serializer_class = SimpleUserSerilaizer
	pagination_class = None
	def get_queryset(self):
		usr = get_object_or_404(User, name=self.kwargs["name"])
		customers =  Order.objects.filter(coach = usr).values_list("custom",flat=True)
		return User.objects.filter(name__in = customers).order_by("name")
		#return usr.income_orders.customer
		#return Product.objects.filter(coach=usr)

class ModifyGym(APIView):
	def post(self, request, name):
		usr = get_object_or_404(User, name=self.kwargs["name"])
		newgym = get_object_or_404(Gym,id=request.DATA['gym'])
		usr.gym = [newgym]
		usr.save()
		serializer = GymSerializer(newgym)
		return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
		
	

		
		
