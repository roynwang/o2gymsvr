from django.shortcuts import render
from rest_framework import generics,pagination
from .models import *
from .serializers import *

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
            


class SimpleWorkoutActionList(generics.ListCreateAPIView):
	serializer_class = SimpleWorkoutActionSerializer 
	pagination_class = None
        queryset = SimpleWorkoutAction.objects.all()
        '''
        def get_queryset(self):
            t = WorkoutAction.objects.all()
            for i in t:
                SimpleWorkoutAction.objects.create(name=i.name)
        '''

