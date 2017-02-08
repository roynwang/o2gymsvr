import requests
from django.conf import settings
import json

def get_accesstoken():
	f = open("/root/o2gymsvr/crontab/wxtoken","r")
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

