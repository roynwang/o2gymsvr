from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination 
from crawl.models import *
from crawl.serializers import *


# Create your views here.
class CrawlShopCountList(generics.ListCreateAPIView):
	lookup_field = "keyword"
	queryset = CrawlShopCount.objects.all()
	serializer_class = CrawlShopCountSerializer
        pagination_class = None

