from django.shortcuts import render
from rest_framework import generics,pagination
from .serializers import *

# Create your views here.

class FreeCourseListView(generics.ListCreateAPIView):
	serializer_class = FreeCourseSerializer
	pagination_class = None
	def get_queryset(self):
		#parse by date
		d = self.kwargs.get("date")
		query_day = d[:4] + "-" + d[4:6] + "-" + d[-2:]
		return FreeCourse.objects.filter(day=query_day).order_by("hour")
		

class FreeCourseItemView(generics.RetrieveUpdateDestroyAPIView):
	queryset = FreeCourse.objects.all()
	serializer_class = FreeCourseSerializer

class CouponListView(generics.ListCreateAPIView):	
	serializer_class = CouponSerializer
	def get_queryset(self):
		return Coupon.objects.filter(gym = self.kwargs.get("pk"),customer = self.kwargs.get("customerid")).order_by("-valid_date")
		#parse by date

class CouponItemView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Coupon.objects.all()
	serializer_class = CouponSerializer 

