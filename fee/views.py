from django.shortcuts import render
from rest_framework import generics,pagination
from django.shortcuts import render,get_object_or_404,redirect
from rest_framework.views import APIView 
from .models import *
from .serializers import *
from business.models import *
from rest_framework.response import Response
from usr.models import *
import datetime
import calendar
from django.db.models import Sum
def add_months(sourcedate,months):
	month = sourcedate.month - 1 + months
	year = int(sourcedate.year + month / 12 )
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return datetime.date(year,month,day)


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
		allcoaches = gymitem.coaches.values_list("id", flat=True)
		print allcoaches
		for c in gymfee.coach_salary_setting.all():
			if not c.coach in allcoaches:
				c.delete()
		return Response({"result":"created"})

class CoachSalaryView(APIView):
	def getsale(self,coach,start, end):
		orders = coach.income_orders.filter(paidtime__range=[start,end])
		for order in orders.all():
			print order.paidtime
		sold = orders.aggregate(Sum('amount'))["amount__sum"] or 0
		sold_xu = orders.filter(isfirst=False).aggregate(Sum('amount'))["amount__sum"] or 0
		return {"sold":sold, "sold_xu":sold}

	def get(self, request, gymid):
		gymfee = get_object_or_404(GymFee, gym = self.kwargs["gymid"])
		
		if "end" in request.GET:
			end = datetime.datetime.strptime(request.GET["end"], "%Y%m%d")
		else:
			end = datetime.date.today()

		if "start" in request.GET:
			start = datetime.datetime.strptime(request.GET["start"], "%Y%m%d")
		else:
			start = add_months(end, -1)
		end = end + datetime.timedelta(days=1)

		resp = []
		print start
		print end
		for coach in gymfee.coach_salary_setting.all():
			sl = CoachSalarySettingSerializer(coach)
			tmp = sl.data
			sale = self.getsale(get_object_or_404(User,id=coach.coach),start,end)
			tmp["sale"] = sale
			resp.append(tmp)
			#tmp["sold_income"] = sale["sold"] * coach.xiaoshou / 100
			#tmp["xu_income"] = sale["sold_xu"] * coach.xuke / 100
		return Response(resp)
			
		
		
		
		

