from django.shortcuts import render
from recommend.serializers import *
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from weibo.models import *
from usr.models import *
from business.models import *

# Create your views here.

class RecommendList(generics.ListCreateAPIView):
	queryset = Recommend.objects.all()
	serializer_class = RecommendSerializer

class RecommendItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = Recommend.objects.all()
	serializer_class = RecommendSerializer

class RecommendAdd(APIView):
	def get(self, request, pk, rtype, itemid):
		rlist = get_object_or_404(Recommend, pk=pk)
		typehash = {
				"person": User,
				"gym": Gym,
				"article": Weibo,
				}
		fieldhash = {
				"person": rlist.person,
				"gym": rlist.gym,
				"article": rlist.article,
				}
		print(itemid)
		item = get_object_or_404(typehash[rtype], pk=itemid)
		
		#add to list
		fieldhash[rtype] = item
		rlist.save()

		return Response({"msg": rtype + ": " + str(item.id)}, status = status.HTTP_202_ACCEPTED)

