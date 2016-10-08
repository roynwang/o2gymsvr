# coding=utf-8
from rest_framework import serializers
from weibo.models import *
from usr.serializers import *
from django.shortcuts import render,get_object_or_404
import datetime
import pprint
import pytz


class LongWeiboSerializer(serializers.ModelSerializer):
	class Meta:
		model = LongWeibo

class LongWeiboHtmlSerializer(serializers.ModelSerializer):
	class Meta:
		model = LongWeibo
		fields = ["content"]


class WeiboSerializer(serializers.ModelSerializer):
	class Meta:
		model = Weibo

class WeiboAuthorSerializer(serializers.ModelSerializer):
	author = UserSerializer(source='by', read_only=True)
	coachcontent = CoachSerializer(source="coach",read_only=True) 
	class Meta:
		model = Weibo
 
class ReadWeiboSerializer(serializers.ModelSerializer):
	topcomments = WeiboAuthorSerializer(many=True, source='top_comments')
	author = SimpleUserSerilaizer(source='by', read_only=True)
	fwdcontent = WeiboAuthorSerializer(source="fwdfrom",read_only=True)
	coachcontent = CoachSerializer(source="coach",read_only=True) 
	
	class Meta:
		model = Weibo


class ImageSerializer(serializers.ModelSerializer):
	date = serializers.SerializerMethodField()
	class Meta:
		model = Images
        def get_date(self, obj):
		tz = pytz.timezone('Asia/Chongqing')
                t = obj.created.astimezone(tz)
		return datetime.date.strftime(t,"%Y年%m月%d") 
                 
