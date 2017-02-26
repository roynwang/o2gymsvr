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
import pprint


# Create your views here.
class CrawlShopCountList(generics.ListCreateAPIView):
	queryset = CrawlShopCount.objects.all()
	serializer_class = CrawlShopCountSerializer
        pagination_class = None

class TaskList(generics.ListCreateAPIView):
	queryset = CrawlTask.objects.filter(status="init")
	serializer_class = CrawlTaskSerializer

class LatestTask(generics.RetrieveAPIView):
	serializer_class = CrawlTaskSerializer
	def get_object(self):
            query  =  CrawlTask.objects.filter(status="init").order_by("created")
            if query.count() == 0:
                return None
            ret =  CrawlTask.objects.filter(status="init").order_by("created")[0]
            ret.status = "crawling"
            if ret.url == "":
                q = ret.keyword.replace(" ","+")
                ret.url = "http://t.dianping.com/list/"+ret.city+"?q="+q
            ret.save()
            return ret

class TaskItem(generics.RetrieveUpdateAPIView):
	serializer_class = CrawlTaskSerializer
	queryset = CrawlTask.objects.all()
	def partial_update(self, request, *args, **kwargs):
	    ret = super(TaskItem,self).partial_update(request,args, kwargs)
            item = self.get_object()
            item.handle_list()
            item.status = "done"
            item.save()
            return ret


class TaskItemExtract(APIView):
        def get(self, request, pk):
            item = get_object_or_404(CrawlTask, id=pk)
            '''
            lh = ListHandler(item)
            gl = lh.get_groupon_list()
            pagenum = lh.get_current_page_num()
            links = lh.extract_page_url()
            '''
            item.handle_list()
            return Response({"msg":"ok"})
            

