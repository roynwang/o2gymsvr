from django.shortcuts import render
from rest_framework import generics,pagination
from django.shortcuts import render,get_object_or_404,redirect
from rest_framework.views import APIView 
from .models import *
from .serializers import *
from business.models import *
from rest_framework.response import Response

# Create your views here.
class GymCoachSalarySettingView(generics.ListAPIView):
	pagination_class = None
	serializer_class = CoachSalarySettingSerializer 
	def get_queryset(self):
		gymfee = get_object_or_404(GymFee, gym = self.kwargs["gymid"])
		return CoachSalarySetting.objects.filter(gymfee = gymfee)

class GymCoachSalarySettingItemView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = CoachSalarySettingSerializer 
	lookup_field = "coach"
	def get_queryset(self):
		return GymFee.objects.get(gym=self.kwargs["gymid"]).coach_salary_setting.all()



class GymSync(APIView):
	def get(self,request,gymid):
		#1 create gymfee
		gymfee, _ = GymFee.objects.get_or_create(gym=gymid)
		gymitem = Gym.objects.get(id = gymid)
		for coach in gymitem.coaches.all():
			CoachSalarySetting.objects.get_or_create(
					coach =  coach.id,
					gymfee = gymfee)
		return Response({"result":"created"})

