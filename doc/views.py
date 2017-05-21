# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework import generics
from rest_framework import pagination
from doc.serializers import *

# Create your views here.

class GymDocList(generics.ListCreateAPIView):
	serializer_class = GymDocSerializer
        pagination_class = None
	def get_queryset(self):
            if self.kwargs['gymid'] in ["19","31"]:
                return GymDoc.objects.filter(gym__in=[19,31])
            else:
                return GymDoc.objects.filter(gym=self.kwargs['gymid'])

class GymDocItem(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = GymDocSerializer
        queryset = GymDoc.objects.all()


class GymVideoList(generics.ListCreateAPIView):
	serializer_class = GymVideoSerializer
        pagination_class = None
	def get_queryset(self):
            if self.kwargs['gymid'] in ["19","31"]:
                return GymVideo.objects.filter(gym__in=[19,31])
            else:
                return GymVideo.objects.filter(gym=self.kwargs['gymid'])

class GymVideoListWithPage(generics.ListCreateAPIView):
	serializer_class = GymVideoSerializer
        pagination_class = pagination.PageNumberPagination
	def get_queryset(self):
            if self.kwargs['gymid'] in ["19","31"]:
                return GymVideo.objects.filter(gym__in=[19,31])
            else:
                return GymVideo.objects.filter(gym=self.kwargs['gymid'])


class GymVideoKeywordList(generics.ListCreateAPIView):
	serializer_class = GymVideoKeywordSerializer
        pagination_class = None
        def get_queryset(self):
            return GymVideoKeyword.objects.filter(videoid=self.kwargs['videoid'])
        

class GymVideoKeywordItem(generics.RetrieveDestroyAPIView):
        lookup_field = "keyword"
        serializer_class = GymVideoKeywordSerializer
        def get_queryset(self):
            t = self.kwargs['keyword'].encode("utf8")
            m =  GymVideoKeyword.objects.filter(keyword=t,videoid=self.kwargs['videoid'])
            return m


