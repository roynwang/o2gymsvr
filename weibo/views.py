# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response
from weibo.models import *
from weibo.serializers import *
from usr.models import *
from rest_framework import status
from rest_framework.views import APIView
from qiniu import Auth, BucketManager
import json
import pprint
from django.conf import settings
import os
import uuid

from rest_framework.decorators import api_view,renderer_classes
from utils import wxutils

# Create your views here.


class WeiboListAll(generics.ListCreateAPIView):
	queryset = Weibo.objects.all()
	serializer_class = ReadWeiboSerializer

class WeiboList(generics.ListCreateAPIView):
	queryset = Weibo.objects.all()
	serializer_class = ReadWeiboSerializer

	def pushtofeed(self, tl, wb):
		tl.feed.add(wb)
		tl.refresh.add(wb)

	def get_queryset(self):
		by = self.kwargs.get('by')
		queryset = Weibo.objects.filter(by=by)
		return queryset

	def saveimg(self, usr, imgs):
		if not imgs:
			return
		imgset = json.loads(imgs)
		for img in imgset:
			print("saving img " + img)
			dbimg = Images.objects.create(url=img, by=usr)

	def create(self, request, *args, **kwargs):
		#pprint.pprint(request.data)
		#by = TimeLine.objects.get(name=self.kwargs.get('by'))

		usr = get_object_or_404(User, name=self.kwargs.get('by'))
		by, created = TimeLine.objects.get_or_create(name=usr)
                if created:
     		    by.followedby.add(by)
    		    by.save()
		#check whether the 'by' field is them same as url parameter 
		#if  unicode(by.id) != request.data.get('by'):
		#	return Response({"error":"author mismatch"}, status=status.HTTP_400_BAD_REQUEST)
		serializer = WeiboSerializer(data=request.data)
		if serializer.is_valid():
			wb = serializer.save()
			#save pic
			self.saveimg(usr, wb.imgs)
			if wb.isfwd == True:
				usr.fwded.add(wb.fwdfrom)
				wb.fwdfrom.fwdnum += 1
				wb.fwdfrom.save()
				if wb.fwdfrom.isfwd == True:
					usr.fwded.add(wb.fwdfrom.fwdfrom)
					#update fwdfrom to original post
					wb.fwdfrom = wb.fwdfrom.fwdfrom
					wb.fwdfrom.fwdnum += 1
					wb.save()
				usr.save()
				wb.fwdfrom.save()
			if wb.iscomments == True:
				#handle comments number
				wb.commentto.commentnum = wb.commentto.commentnum + 1
				wb.commentto.save()
			else:
				#self.pushtofeed(by,wb)
				for flw  in by.followedby.all():
					self.pushtofeed(flw,wb)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeiboItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = Weibo.objects.all()
	serializer_class = ReadWeiboSerializer

class History(generics.ListAPIView):
	queryset = Weibo.objects.all()
	serializer_class = WeiboSerializer

class CommentList(generics.ListCreateAPIView):
	serializer_class = ReadWeiboSerializer
	def get_queryset(self):
		weiboid = self.kwargs.get("weiboid")
		queryset = Weibo.objects.get(id=weiboid).comments.all()
		return queryset

class WeiboUp(APIView):
	def get(self, request, by, weiboid, upaction):
		print self.kwargs
		usr = get_object_or_404(User, name=by)
		weibo = get_object_or_404(Weibo, pk = weiboid)
		if upaction == 'up':
			print("xxxxxxxxxxxxxxxx")
			weibo.upnum = weibo.upnum + 1
			usr.upped.add(weibo)
			if weibo.isfwd:
				weibo.fwdfrom.upnum += 1
				usr.upped.add(weibo.fwdfrom)
				weibo.fwdfrom.save()
		else:
			weibo.upnum = weibo.upnum - 1
			usr.upped.remove(weibo)
			if weibo.isfwd:
				weibo.fwdfrom.upnum -= 1
				usr.upped.remove(weibo.fwdfrom)
				weibo.fwdfrom.save()
		weibo.save()
		serializer = WeiboSerializer(weibo)
		return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

class LongWeiboList(generics.ListCreateAPIView):
	queryset = LongWeibo.objects.all().order_by("-id")
	serializer_class = LongWeiboSerializer

class LongWeiboItem(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = "weiboid"
	queryset = LongWeibo.objects.all()
	serializer_class = LongWeiboSerializer

class PicFetch(APIView):
	def get(self,request):
		mediaid = request.query_params["mediaid"]
		filename = str(uuid.uuid1()).replace("-","") + ".jpg"
		q = Auth(settings.QNACCESSKEY, settings.QNSECRETKEY)
		bucket = BucketManager(q)
		token = wxutils.get_accesstoken()
		mediaurl = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=" + token + "&media_id=" + mediaid
		ret, info = bucket.fetch(mediaurl,settings.QNBUKET,filename)
		return Response({"pic": filename})



class PicToken(APIView):
	def get(self,request):
		q = Auth(settings.QNACCESSKEY, settings.QNSECRETKEY)
                if "filename" in request.query_params:
                    filename = request.query_params['filename']
                else:
		    filename = str(uuid.uuid1()).replace("-","") + ".jpg"

		print(filename)
		token = q.upload_token(settings.QNBUKET, filename)
		print(token)
		return Response({"key":filename, "token":token}, status=status.HTTP_202_ACCEPTED)


class ArticlePage(APIView):
	renderer_classes = (StaticHTMLRenderer,)
	permission_classes = (AllowAny,)
	def get(self, reqesut, weiboid):
		article = get_object_or_404(LongWeibo, weiboid=weiboid)
		return Response(article.content)

class ImageItem(generics.RetrieveDestroyAPIView):
	#queryset = Images.objects.all()
	serializer_class = ImageSerializer 
	def get_queryset(self):
		usr = get_object_or_404(User, id=self.kwargs.get("by"))
		return Images.objects.all().filter(by=usr).order_by("-created")
