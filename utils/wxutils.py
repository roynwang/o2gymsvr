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

def get_openid(code):
	params = {"appid":"wxf1aacfc6230603e8",\
		"secret": "194968558f73dd78750095ad5ec69796",\
                "js_code":code,\
                "grant_type":"authorization_code"}
        url = "https://api.weixin.qq.com/sns/jscode2session?appid=wxf1aacfc6230603e8&secret=194968558f73dd78750095ad5ec69796&js_code="+code+"&grant_type=authorization_code"
        resp = requests.get(url)
        res = resp.json()

        if "openid" in res:
    	    return resp.json()["openid"]
        return False

