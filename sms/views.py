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

import base64
import datetime
import urllib2
import md5
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login	
from utils import smsutils

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
	auth_usr.set_password(pwd)
	auth_usr.save()
	payload = jwt_payload_handler(auth_usr)
	return {'token':jwt_encode_handler(payload)}

@permission_classes((AllowAny, ))
class PwdLogin(APIView):
	def login_with_pwd(self,request):
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		print request.POST
		username = request.POST['username']
		password = request.POST['password']
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
		num, _ =  Sms.objects.get_or_create(number=request.DATA["number"])
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
		print request.DATA
		if str(sms.vcode) == request.DATA["vcode"]:
			ret = Response(get_or_create_user_return_token(number, request.DATA["password"]) , status=status.HTTP_200_OK)
			#generate token
			sms.vcode = randint(100000,999999)
			sms.save()
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
		
