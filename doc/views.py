from django.shortcuts import render
from rest_framework import generics
from doc.serializers import *

# Create your views here.

class GymDocList(generics.ListCreateAPIView):
	serializer_class = GymDocSerializer
        pagination_class = None
	def get_queryset(self):
            return GymDoc.objects.filter(gym=self.kwargs['gymid'])

class GymVideoList(generics.ListCreateAPIView):
	serializer_class = GymVideoSerializer
        pagination_class = None
	def get_queryset(self):
            return GymVideo.objects.filter(gym=self.kwargs['gymid'])
