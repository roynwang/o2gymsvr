from django.shortcuts import render
from rest_framework import generics,pagination
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.core.cache import cache
import json


# Create your views here.
class WorkoutCategeoryList(generics.ListCreateAPIView):
	queryset = WorkoutCategeory.objects.all()
	serializer_class = WorkoutCategeorySerializer 
	pagination_class = None

class WorkoutActionList(generics.ListCreateAPIView):
	serializer_class = WorkoutActionSerializer 
	pagination_class = None
	def get_queryset(self):
		cate = get_object_or_404(WorkoutCategeory, id=self.kwargs.get("cate"))
		by = self.kwargs.get("name")
		return WorkoutAction.objects.filter(categeory = cate, by__in = [by, ""])

class CustomerWorkoutValueItem(generics.RetrieveAPIView):
	serializer_class = SimpleWorkoutActionSerializer 
        def get_object(self):
            customer = self.kwargs.get("customer")
            workoutid = self.kwargs.get("workoutid")
            return get_object_or_404(CustomerWorkoutValue,customer=customer,workoutid=workoutid) 

class SimpleWorkoutItem(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = SimpleWorkoutActionSerializer 
        lookup_field = "pk"
        queryset = SimpleWorkoutAction.objects.all()


class SimpleWorkoutActionListSmart(generics.ListCreateAPIView):
	serializer_class = SimpleWorkoutActionSerializer 
	pagination_class = None
        queryset = SimpleWorkoutAction.objects.all()


        def get_last_used(self,name):
            detail = cache.get("o2_coachaction_" + name)
            if detail is None:
                return []
            actions = json.loads(detail)
            used = []
            for item in actions:
                if item["contenttype"] == "action":
                    used.append(item['workoutid'])
            return used

        def list(self, request, name):
            t = SimpleWorkoutAction.objects.all()
            s = self.get_serializer(t, many=True)
            jd = s.data
            ret = []
            used = self.get_last_used(name)
            for item in jd:
                if item['id'] in used:
                    ret.insert(0,item)
                else:
                    ret.append(item)
            return Response(ret)
           


class SimpleWorkoutActionList(generics.ListCreateAPIView):
	serializer_class = SimpleWorkoutActionSerializer 
	pagination_class = None
        queryset = SimpleWorkoutAction.objects.all()

        '''
	def create(self, request, *args, **kwargs):
            print request.data
	    ret = super(ScheduleList, self).create(request, args,kwargs)
            return ret
        '''
            
        '''
        def get_queryset(self):
            t = WorkoutAction.objects.all()
            for i in t:
                SimpleWorkoutAction.objects.create(name=i.name)
        '''

class NewSimpleWorkoutActionList(generics.ListCreateAPIView):
	serializer_class = NewSimpleWorkoutActionSerializer 
	pagination_class = None
        queryset = NewSimpleWorkoutAction.objects.all()

class CustomerTargetList(generics.ListCreateAPIView):
	serializer_class = CustomerTargetSerializer 
	pagination_class = None
        def get_queryset(self):
            return CustomerTarget.objects.filter(customer=self.kwargs.get("customer"))

class CustomerTargetItem(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = CustomerTargetSerializer
        lookup_field = "pk"
        queryset = CustomerTarget.objects.all()

