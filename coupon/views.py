from django.shortcuts import render, get_object_or_404
from rest_framework import generics,pagination
from .serializers import *
from rest_framework.response import Response
from usr.models import *

# Create your views here.

class FreeCourseListView(generics.ListCreateAPIView):
	serializer_class = FreeCourseSerializer
	pagination_class = None
	def get_queryset(self):
		#parse by date
		d = self.kwargs.get("date")
		query_day = d[:4] + "-" + d[4:6] + "-" + d[-2:]
		return FreeCourse.objects.filter(day=query_day).order_by("hour")

class CustomerFreeCourseItemView(generics.RetrieveUpdateDestroyAPIView):
	queryset = FreeCourse.objects.all()
	serializer_class = FreeCourseSerializer
	def get_object(self):
		return get_object_or_404(FreeCourse, customer=self.kwargs["customer"])

class CoachFreeCourseListView(generics.ListAPIView):
	serializer_class = FreeCourseSerializer
	pagination_class = None
	def get_queryset(self):
		coach = get_object_or_404(User, name=self.kwargs["pk"])
		return FreeCourse.objects.filter(coach=coach.id).order_by("hour")
		

class FreeCourseItemView(generics.RetrieveUpdateDestroyAPIView):
	queryset = FreeCourse.objects.all()
	serializer_class = FreeCourseSerializer

	def partial_update(self, request, *args, **kwargs):
		customer = int(request.data["customer"])
		tar = FreeCourse.objects.get(id=kwargs["pk"])		
		if customer == -1:
			tar.sealed = 0
			tar.customer = None
			tar.save()
			return Response({'msg':'success'}) 

		if tar.sealed == 1:
			return Response({"error":"sealed"})
		found = FreeCourse.objects.filter(customer=customer).count()
		if found:
			return Response({"error":"existed"})
		tar.customer = customer
		tar.sealed = 1
		tar.save()
		return Response({'msg':'success'}) 

class CouponListView(generics.ListCreateAPIView):	
	serializer_class = CouponSerializer
	def get_queryset(self):
		return Coupon.objects.filter(gym = self.kwargs.get("pk"),customer = self.kwargs.get("customerid")).order_by("-valid_date")
		#parse by date

class CouponItemView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Coupon.objects.all()
	serializer_class = CouponSerializer 

	
		

