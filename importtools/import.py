import json
import sys
import requests

def sendReq(phone,params):
	resp = requests.post("http://o2-fit.com/api/"+phone+"/manualorder/", params)
	return resp.json()


def createBook(resp,datestr,hour):
	print resp
	coachphone = resp["coachdetail"]["name"]
	coachid = resp["coachdetail"]["id"]

	customerphone = resp["customerdetail"]["name"]
	customerid = resp["customerdetail"]["id"]
	orderid = resp["id"]

	data = {"coach":coachid, "custom":customerid, "order":orderid,"hour":hour,
			"date":datestr,"done":True}
	url = "http://o2-fit.com/api/" + coachphone + "/b/" + datestr.replace("-","") + "/"
	print "xxxxxxxxxxxxxxx"
	print json.dumps(data)
	print "xxxxxxxxxxxxxxx"
	resp = requests.post(url, data)
	return resp

def buildOrderParam(line):
	arr = line.split("\t")
	return {"customer_displayname":arr[0],\
			"customer_phone": arr[2],\
			"product_introduction":"dummy",\
			"product_price":arr[5],\
			"product_promotion":-1,\
			"product_amount":arr[4],\
			"product_duration":0,\
			"sex": arr[1],\
			"age":0,\
			"subsidy":0,\
			"birthday":arr[3]}

def execute(line):
	orderparam = buildOrderParam(line)
	order = sendReq("15101089789", orderparam)
	#order = sendReq("18311286007", orderparam)
	arr = line.split("\t")
	for i in range(0,int(arr[-1])):
		print createBook(order, "2015-01-01",1).text.encode("utf-8")

if __name__ == '__main__':
	f = open("zhongguancun.csv","r")
	for line in f.readlines():
		execute(line)
