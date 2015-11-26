# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from usr.models import *
from business
import re 
import datetime

class WxView(APIView):
	def bindwx(self, openid,phone):
		if User.objects.filter(name=phone).exists():
			usr = User.objects.get(name=phone)
			usr.openid = openid
			usr.save()
			return True
		else:
			return False
	def completeCourse(self,openid):
		#if openid has not been registered then return need to bind phone
		if not User.objects.filter(openid=openid).exists():
			return '首次使用请回复您的电话号码以确认课程完成(下次就不用了哦～）'
		else:
			# complete the book today
			today = ""
			usr = User.objects.get(openid=openid)
			for s in Schedule.objects.filter(date=today, custom = usr):
				s.done()
			return "确认课程成功"

	def post(self, request):
		try:
			wechat_instance.parse_data(data=request.body)
		except ParseError:
			return HttpResponseBadRequest('Invalid XML Data')

		# 获取解析好的微信请求信息
		message = wechat_instance.get_message()

		# 关注事件以及不匹配时的默认回复
		reply_text = '感谢您的关注！\n回复您的电话号码（11位）以链接你氧气健身数据'
		if isinstance(message, TextMessage):
				# 当前会话内容
			content = message.content.strip()
			if re.match("\d{11}",content) and self.bindwx(message.source, content):
				reply_text  = self.completeCourse(message.source):
			else:
				reply_text = '手机绑定失败'
		elif message.type in ["subscribe", "scan"]:
			return self.completeCourse(message.source)
		else:
			reply_text = '感谢您的关注！\n回复您的电话号码（11位）以链接你氧气健身数据'
		response = wechat_instance.response_text(content=reply_text)
		return HttpResponse(response, content_type="application/xml")

