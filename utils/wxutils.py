import requests
from django.conf import settings

def get_accesstoken():
	params = {"grant_type":"client_credential",\
			"appid":settings.WECHAT_APPID,\
			"secret": settings.WECHAT_APPSECRET}
	resp = requests.get(settings.WECHAT_TICKETURL,params)
	return resp.json()["access_token"]

