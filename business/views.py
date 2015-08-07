from django.shortcuts import render
from business.models import *
from business.serializers import *
from rest_framework import generics

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
