import requests
from django.conf import settings
import json
import urllib
import urllib2
import requests
import random
import hashlib
import socket
import sys
import xmltodict


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
 
 
def GetHostIpAddr():
    name = socket.getfqdn(socket.gethostname())
    addr = socket.gethostbyname(name)
    return addr
 
def GetRandomStr():    
    m2 = hashlib.md5()   
    m2.update(str(random.randint(10000, 99999999999999999)))   
    result = m2.hexdigest()    
    return result.upper()

def getSign(data, appkey = "76e238bd3759d59d6582da47b7d65eae"):
    signature = '&'.join(['%s=%s' % (key, data[key]) for key in sorted(data)])
    signature += "&key="
    signature += appkey
    m2 = hashlib.md5()   
    m2.update(signature)
    return m2.hexdigest().upper()
 
def XmlData(orderid,openid,title, price, ip, callbackurl, key):
    appidvalue = "wxf1aacfc6230603e8" #appid
    attachvalue ="o2_pay"
    mch_idvalue = "1334658401" #mch_id
    nonce_strvalue = GetRandomStr()
    bodyvalue = title
    out_trade_novalue = orderid
    total_feevalue = str(price)    
    spbill_create_ipvalue = ip
    notify_urlvalue = callbackurl 
    trade_typevalue = "JSAPI"
    keyvalue = key
    openidvalue=openid
     
    formatstr = 'appid=%s&attach=%s&body=%s&mch_id=%s&nonce_str=%s&notify_url=%s&openid=%s&out_trade_no=%s'\
    '&spbill_create_ip=%s&total_fee=%s&trade_type=%s&key=%s'%(appidvalue,attachvalue,bodyvalue,mch_idvalue,nonce_strvalue,\
    notify_urlvalue,openidvalue,out_trade_novalue,spbill_create_ipvalue,total_feevalue,trade_typevalue,keyvalue)
    #print formatstr
         
    mobj = hashlib.md5()   
    mobj.update(formatstr)
    signvalue = mobj.hexdigest()
    signvalue = signvalue.upper()
     
    xmlstart = "<xml>\r\n"
    appid = "<appid>"+appidvalue+"</appid>\r\n"
    attach = "<attach>"+attachvalue+"</attach>\r\n"
    body = "<body>"+bodyvalue+"</body>\r\n"
    mch_id = "<mch_id>"+mch_idvalue+"</mch_id>\r\n"
    nonce_str = "<nonce_str>"+nonce_strvalue+"</nonce_str>\r\n"
    notify_url = "<notify_url>"+notify_urlvalue+"</notify_url>\r\n"
    openid = "<openid>"+openidvalue+"</openid>\r\n"
    out_trade_no ="<out_trade_no>"+str(out_trade_novalue)+"</out_trade_no>\r\n"
    spbill_create_ip = "<spbill_create_ip>"+spbill_create_ipvalue+"</spbill_create_ip>\r\n"
    total_fee = "<total_fee>"+total_feevalue+"</total_fee>\r\n"
    trade_type = "<trade_type>"+trade_typevalue+"</trade_type>\r\n"
    sign = "<sign>"+signvalue+"</sign>\r\n"
    xmlend = "</xml>"
    result = xmlstart+appid+attach+body+mch_id+nonce_str+notify_url+openid+out_trade_no+spbill_create_ip+total_fee+trade_type+sign+xmlend
    print result
    #print result
    return result
     
def Post(data):
    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    headers = {"Content-Type":"text/xml"}
    rep = urllib2.Request(url=url,headers =headers,data=data)
    response = urllib2.urlopen(rep)
    res = response.read()
    return xmltodict.parse(res);
    #return res

def create_charge(billid,openid,title,amount,ip):
    callback = "https://o2-fit.com/api/pay/chargecallback/"
    key = "76e238bd3759d59d6582da47b7d65eae"
    return Post(XmlData(billid,openid,title,amount*100,ip,callback,key))
    
'''
if __name__ == "__main__":
    #print Post(XmlData("123511654189415","openid","title",1000,"192.168.1.1","http://callback","mmmmmmmmmmmmmmmmmmm"))
    #print create_charge("1233423423423424","obzf70EAA4fBncDhQwe9z24l19es","title",1000, "192.168.1.1")
    data = {"appId":"wxf1aacfc6230603e8",\
            "nonceStr":"60B4E38272B8FEB2F34080AD1D393D45",\
            "package":"prepay_id=wx201702221817403823c1747f0407516639",\
            "signType":"MD5","timeStamp":"1487758660"}
    signature = getSign(data)
    print signature
'''
