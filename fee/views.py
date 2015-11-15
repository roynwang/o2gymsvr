from django.shortcuts import render
from rest_framework import generics,pagination
from django.shortcuts import render,get_object_or_404,redirect
from rest_framework.views import APIView 
from .models import *
from .serializers import *
from business.models import *
from rest_framework.response import Response
from usr.models import *
from datetime import date, datetime, timedelta
from django.db.models import Sum

# Create your views here.
class GymCoachSalarySettingView(generics.ListAPIView):
	pagination_class = None
	serializer_class = CoachSalarySettingSerializer 
	def get_queryset(self):
		gymfee = get_object_or_404(GymFee, gym = self.kwargs["gymid"])
		return CoachSalarySetting.objects.filter(gymfee = gymfee)

class GymCoachSalarySettingItemView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = CoachSalarySettingSerializer 
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

class CoachSalaryView(APIView):
	def getsale(self,coach,start, end):
		orders = coach.income_orders.filter(paidtime__range=[start,end])
		sold = orders.aggregate(Sum('amount'))["amount__sum"] or 0
		sold_xu = orders.filter(isfirst=False).aggregate(Sum('amount'))["amount__sum"] or 0
		return {"sold":sold, "sold_xu":sold}

	def get(self, request, gymid):
		gymfee = get_object_or_404(GymFee, gym = self.kwargs["gymid"])
		end = date.today() + timedelta(days=1)
		start = end - timedelta(days=30)
		resp = []
		for coach in gymfee.coach_salary_setting.all():
			sl = CoachSalarySettingSerializer(coach)
			tmp = sl.data
			sale = self.getsale(get_object_or_404(User,id=coach.coach),start,end)
			tmp["sale"] = sale
			resp.append(tmp)
			#tmp["sold_income"] = sale["sold"] * coach.xiaoshou / 100
			#tmp["xu_income"] = sale["sold_xu"] * coach.xuke / 100
		return Response(resp)
			
		
		
		
		

