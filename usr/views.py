from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


from usr.models import *
from usr.serializers import *
from weibo.serializers import *

import pprint


class UserList(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	def create(self, request, *args, **kwargs):
		resp = super(UserList, self).create(request, args, kwargs)
		tl = TimeLine.objects.create(name=get_object_or_404(User, name=request.data["name"]))
		tl.followedby.add(tl)
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
	def get_queryset(self):
		return User.objects.get(name=self.kwargs.get('name')).album.all()

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

