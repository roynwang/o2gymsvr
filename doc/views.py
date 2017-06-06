# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView 
from rest_framework import pagination
from rest_framework import status
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

class GymVideoItem(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = GymVideoSerializer
        queryset = GymVideo.objects.all()



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
                return GymVideo.objects.filter(gym__in=[19,31]).order_by("-id")
            else:
                return GymVideo.objects.filter(gym=self.kwargs['gymid']).order_by("-id")


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


class GymVideoCrawl(APIView):
    def get(self, request,pk):
        file_object = open('./crontab/workout/'+ str(pk))
        try:
            all_the_text = file_object.read( )
            j = json.loads(all_the_text)
            if not 'id' in j:
                return Response({'content':'invalid'}, status=status.HTTP_404_NOT_FOUND)
            obj = GymVideo.objects.create(id=int(j['id']),\
                    gym = 31,\
                    uploader="虞柳河",\
                    coach="虞柳河",\
                    title=j['name'],\
                    summary=j['description'],\
                    attachment=j['video_url'],\
                    pic=j['pic'],\
                    datestr="2017-06-06",\
                    update = datetime.datetime.now())
	    serializer = GymVideoSerializer(obj)
	    return Response(serializer.data, status=status.HTTP_201_CREATED)

        finally:
            file_object.close( )

