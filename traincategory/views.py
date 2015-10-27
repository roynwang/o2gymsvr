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
