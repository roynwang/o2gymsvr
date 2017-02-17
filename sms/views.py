# coding=utf-8
from django.shortcuts import render,get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import json
from random import randint
from sms.models import *
from usr.models import *
from .serializers import *
from django.contrib.auth import get_user_model
from business.models import *
import random
import hashlib
import string
import pprint

import base64
import datetime
import urllib2
import md5
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login	
from utils import smsutils

from django.http import HttpResponse
import hashlib, time, re
from xml.etree import ElementTree as ET
import requests
from qiniu import Auth, BucketManager
from utils import wxutils


def get_or_create_user_return_token(number,pwd):
	print "----------"
	jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
	jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
	try:
		usr = User.objects.get(name=number)
	except:
		usr = None
	try:
		auth_usr = get_user_model().objects.get(username=number)
	except:
		auth_usr = None
	print "----------"
	print auth_usr
	if not usr:
		print "creating user"
		usr = User.objects.create(name=number,
				displayname=number,
				avatar=settings.DEFAULT_AVATAR
				)
		#create timeline and working hours

		print "creating tl"
		tl = TimeLine.objects.create(name=usr)
		tl.followedby.add(tl)
		tl.save()
		wh = WorkingDays.objects.create(name=number)
	if not auth_usr:
		auth_usr = get_user_model().objects.create_user(username=number)
	if pwd != None:
		auth_usr.set_password(pwd)
	auth_usr.save()
	payload = jwt_payload_handler(auth_usr)
	return {'token':jwt_encode_handler(payload)}

@permission_classes((AllowAny, ))
class PwdLogin(APIView):
	def login_with_pwd(self,request):
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		print request.data
		username = request.data['username']
		password = request.data['password']
		user = authenticate(username=username, password=password)
		print "1111111111"
		if user is not None:
			print "22222"
			#login(request, user)
			payload = jwt_payload_handler(user)
			return Response({'token':jwt_encode_handler(payload)})
		else:
			return Response({"result":"failed"}, status=status.HTTP_403_FORBIDDEN)
	def post(self,request):
		print("xxxxxxxxxxxxxxxxxx")
		return self.login_with_pwd(request)


@permission_classes((AllowAny, ))
class SMSGet(generics.CreateAPIView):
	pagination_class = None
	queryset = Sms.objects.all()
	serializer_class = SmsVcodeSerializer 
	def create(self, request, *args, **kwargs):
		vcode = randint(100000,999999)
		num, _ =  Sms.objects.get_or_create(number=request.data["number"])
		num.vcode = vcode
		num.save()
		resp = smsutils.templateSMS(settings.UCPAASSID,
				settings.UCPAASTOKEN,
				settings.UCPAASAPPID,
				num.number,
				settings.UCPAASTEMPLATE,
				str(vcode) + "," + "2")

		print resp
		serializer = SmsVcodeSerializer(num)
		return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class SMSVerify(APIView):
	def post(self,request,number):
		print "xxxxxxxxxxxxx"
		sms = get_object_or_404(Sms,number=number)
		ret = None
		print request.data
		print str(sms.vcode)
		print request.data["vcode"]
		if str(sms.vcode) == request.data["vcode"]:
			sms.vcode = randint(100000,999999)
			sms.save()
			pwd = None
			if "password" in request.data:
				pwd = request.data["password"]
    			ret = Response(get_or_create_user_return_token(number, pwd) , status=status.HTTP_200_OK)

                        if "openid" in request.data:
    		            usr = User.objects.get(name=number)
                            usr.openid = request.data["openid"]
                            usr.save()
		else:
			ret = Response({"result":"failed"}, status=status.HTTP_403_FORBIDDEN)
		return ret

@permission_classes((AllowAny, ))
class GymReg(APIView):
	def post(self,request):
		number = request.data["phone"]
		sms = get_object_or_404(Sms,number=number)
		if str(sms.vcode) == request.data["vcode"]:
			if "password" in request.data:
				get_or_create_user_return_token(number, request.data["password"])
			#create gym here
			gym = Gym.objects.create(
					name=request.data["gymname"],
					introduction="",
					address=request.data["gymaddr"],
					phone=request.data["gymphone"],
					mapid=0,
					imgs="[]",
					)
			#change gym here
			usr = get_object_or_404(User,name=number)
			if "displayname" in request.data:
				usr.displayname = request.data["displayname"]
				usr.gym = [gym]
			usr.role = "admin"
			corps = json.loads(usr.corps)
			corps.append(gym.id)
			usr.corps = json.dumps(corps)

			usr.iscoach = True
			usr.save()
			print "44444"
			sms.vcode = randint(100000,999999)
			sms.save()
			return Response({"result":"success"})
		else:
			return Response({"result":"failed"}, status=status.HTTP_403_FORBIDDEN)


class WechatSignature(APIView):
	def nonceStr(self, length):
		"""随机数"""
		return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
	def jsapiTicket(self,access_token):
		print "token"
		print access_token
		_JSAPI_URL = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi"
		return requests.get(_JSAPI_URL.format(access_token)).json()["ticket"]

	def jsapiSign(self, access_token, url):
		"""jsapi_ticket 签名"""
		ticket = self.jsapiTicket(access_token)
		sign = {
				'nonceStr': self.nonceStr(15),
				'jsapi_ticket': ticket,
				'timestamp': int(time.time()),
				'url': url,
				}
		print "ticket"
		print ticket
		signature = '&'.join(['%s=%s' % (key.lower(), sign[key]) for key in sorted(sign)])
		sign["signature"] = hashlib.sha1(signature).hexdigest()
		sign["appId"] = settings.WECHAT_APPID
		sign["debug"] = True
		return sign
	def get_accesstoken(self):
		params = {"grant_type":"client_credential",\
				"appid":settings.WECHAT_APPID,\
				"secret": settings.WECHAT_APPSECRET}
		resp = requests.get(settings.WECHAT_TICKETURL,params)
		return resp.json()["access_token"]

	def post(self, request):
		url=request.data["url"]
		return Response(self.jsapiSign(wxutils.get_accesstoken(), url))

        def get(self, request):
                pprint.pprint(request.GET)
                code = request.GET.get("code");
                openid = wxutils.get_openid(code)
                if openid:
                    encoded = hashlib.sha1(openid).hexdigest()
                    return Response({"openid": encoded})
		return Response({"result":"failed"}, status=status.HTTP_404_NOT_FOUND)


class Wechat(APIView):
	def get(self,request):
		token = "roynwang"
		params = request.GET
		args = [token, params['timestamp'], params['nonce']]
		args.sort()
		if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
			if params.has_key('echostr'):
				return HttpResponse(params['echostr'])
			else:
				reply = """<xml>
				<ToUserName><![CDATA[%s]]></ToUserName>
				<FromUserName><![CDATA[%s]]></FromUserName>
							<CreateTime>%s</CreateTime>
							<MsgType><![CDATA[text]]></MsgType>
							<Content><![CDATA[%s]]></Content>
							<FuncFlag>0</FuncFlag>
					</xml>"""
				if request.raw_post_data:
					xml = ET.fromstring(request.raw_post_data)
					content = xml.find("Content").text
					fromUserName = xml.find("ToUserName").text
					toUserName = xml.find("FromUserName").text
					postTime = str(int(time.time()))
					if not content:
						return HttpResponse(reply % (toUserName, fromUserName, postTime, "输入点命令吧..."))
					if content == "Hello2BizUser":
						return HttpResponse(reply % (toUserName, fromUserName, postTime, "查询成绩绩点请到http://chajidian.sinaapp.com/ 本微信更多功能开发中..."))
					else:
						return HttpResponse(reply % (toUserName, fromUserName, postTime, "暂不支持任何命令交互哦,功能开发中..."))
				else:
					return HttpResponse("Invalid Request")
		else:
			return HttpResponse("Invalid Request")
