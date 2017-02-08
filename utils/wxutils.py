import requests
from django.conf import settings
import json

def get_accesstoken():
	f = open("../crontab/wxtoken","r")
	line = f.read()
	f.close()
	return json.loads(line)["access_token"]

	'''
	params = {"grant_type":"client_credential",\
			"appid":settings.WECHAT_APPID,\
			"secret": settings.WECHAT_APPSECRET}
	resp = requests.get(settings.WECHAT_TICKETURL,params)
	return resp.json()["access_token"]
	'''

def get_openid(code):
	params = {"grant_type":"authorization_code",\
			"appid":"wxf1aacfc6230603e8",\
                        "js_code":code,\
			"secret": "194968558f73dd78750095ad5ec69796"}
        resp = requests.get("https://api.weixin.qq.com/sns/jscode2session",params)
	return resp.json()["openid"]

