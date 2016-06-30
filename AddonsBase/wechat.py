from xmltodict import parse
from django.http import HttpResponse
import json
import time
def reply_main(data,id):
	data = getdata(data)
	reply =  {}
	reply['ToUserName'] = data['FromUserName']
	reply['FromUserName'] = data['ToUserName']
	reply['Content'] = 'get a request with' + data['MsgType']
	return reply_text(reply)
def getdata(body):
	body = body.decode(encoding = 'utf-8')
	try:
		data = json.loads(json.dumps(parse(body,force_cdata=True)))
	except Exception as e:
		return None
	if(len(data) < 1):
		return None
	data = data['xml']
	temp = {}
	for x in data.keys():
		temp[x] = data[x]['#text']
	return temp

def reply_text(data):
	 extTpl = '''<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName>
	 <CreateTime>%s</CreateTime>
	 <MsgType><![CDATA[%s]]></MsgType>
	 <Content><![CDATA[%s]]></Content>
	 </xml>'''
	 extTpl = extTpl %(data['ToUserName'],data['FromUserName'],str(int(time.time())),'text',data['Content'])
	 return extTpl