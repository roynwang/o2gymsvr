import base64
import datetime
import urllib2
import md5
from django.conf import settings



BOOKSMSTEMPLATE=17152
TimeMap = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00"]

def getSig(accountSid,accountToken,timestamp):
	sig = accountSid + accountToken + timestamp
	return md5.new(sig).hexdigest().upper()

def getAuth(accountSid,timestamp):
	src = accountSid + ":" + timestamp
	return base64.encodestring(src).strip()

def urlOpen(req,data=None):
	try:
		res = urllib2.urlopen(req,data)
		data = res.read()
		res.close()
	except urllib2.HTTPError, error:
		data = error.read()
		error.close()
	return data

def createHttpReq(req,url,accountSid,timestamp,responseMode,body):
	req.add_header("Authorization", getAuth(accountSid,timestamp))
	print "Auth:"
	print getAuth(accountSid, timestamp)
	if responseMode:
		req.add_header("Accept","application/"+responseMode)
		req.add_header("Content-Type","application/"+responseMode+";charset=utf-8")
	if body:
		req.add_header("Content-Length",len(body))
		req.add_data(body)
	print req
	return req

def templateSMS(accountSid,accountToken,appId,toNumbers,templateId,param,isUseJson=True):
	now = datetime.datetime.now()
	timestamp = now.strftime("%Y%m%d%H%M%S")
	signature = getSig(accountSid,accountToken,timestamp)
	url = settings.UCPAASHOST + ":" + settings.UCPAASPORT + "/" + settings.UCPAASSOFTVER + "/Accounts/" + accountSid + "/Messages/templateSMS?sig=" + signature
	print url
	if isUseJson == True:
		body = '{"templateSMS":{ "appId":"%s","to":"%s","templateId":"%s","param":"%s"}}'%(appId,toNumbers,templateId,param)
		print body
		responseMode = "json"
	else:
		body = "<?xml version='1.0' encoding='utf-8'?>\
				<templateSMS>\
				<appId>%s</appId>\
				<to>%s</to>\
				<templateId>%s</templateId>\
				<param>%s</param>\
				</templateSMS>\
				"%(appId,toNumbers,templateId,param)
		responseMode = "xml"
	req = urllib2.Request(url)
	return urlOpen(createHttpReq(req,url,accountSid,timestamp,responseMode,body))

def sendBookNotification(book):

	return
	accountSid = settings.UCPAASSID
	accountToken = settings.UCPAASTOKEN
	appId = settings.UCPAASAPPID
	toNumbers = book.custom.name
	templateId = BOOKSMSTEMPLATE
	#templateId = settings.UCPAASTEMPLATE
	isUseJson = False

	timestr = str(book.date) + " " + TimeMap[book.hour]
	param = ','.join([book.coach.displayname,timestr,book.coach.name,str(4)])
	#param = ','.join([book.coach.displayname,timestr])
	print param
	#return

	now = datetime.datetime.now()
	timestamp = now.strftime("%Y%m%d%H%M%S")
	signature = getSig(accountSid,accountToken,timestamp)
	url = settings.UCPAASHOST + ":" + settings.UCPAASPORT + "/" + settings.UCPAASSOFTVER + "/Accounts/" + accountSid + "/Messages/templateSMS?sig=" + signature
	print url
	if isUseJson == True:
		body = '{"templateSMS":{ "appId":"%s","to":"%s","templateId":"%s","param":"%s"}}'%(appId,toNumbers,templateId,param)
		print body
		responseMode = "json"
	else:
		body = "<?xml version='1.0' encoding='utf-8'?>\
				<templateSMS>\
				<appId>%s</appId>\
				<to>%s</to>\
				<templateId>%s</templateId>\
				<param>%s</param>\
				</templateSMS>\
				"%(appId,toNumbers,templateId,param)
		responseMode = "xml"
	req = urllib2.Request(url)
	return urlOpen(createHttpReq(req,url,accountSid,timestamp,responseMode,body))

	
	

	

