from xmltodict import parse
from django.http import HttpResponse
from .models import Addon,Keyword
from AddonOucJw.views import *
import json
import time
msgdata = {}
openid = ''
token = ''
keyword = ''
def reply_main(request,data,id):
	global msgdata 
	msgdata = getdata(data) #request is to use session
	reply =  {}
	if(keyword == 'subscribe'):
		return 'subscribe'
	elif  msgdata['MsgType'] == 'text' or (msgdata['MsgType'] == 'event' and msgdata['Event'] == 'CLICK'):
		return replymsg(request)
	elif msgdata['MsgType'] == 'voice':
		if 'Recognition' in msgdata.keys():
			return replymsg(request)
		else:
			reply['Content'] = 'I receive the ' + msgdata['keyword']
			return reply_text(reply)
	else:
		reply['Content'] = 'I receive the ' + msgdata['keyword']
		return reply_text(reply)

def replymsg(request):
	reply = {}
	#get the addon from keyword
	addon_name = None
	addon = Keyword.objects.filter(keyword__exact = keyword) # exact
	if len(addon) == 0:# not keyworw
		addon = Keyword.objects.filter(type__exact = '0').filter(keyword__icontains =keyword)
	if len(addon) != 0:
		addon_name = addon[0].addon.name
	if addon_name == 'oucjw':
		reply = oucjwmain(request,msgdata)
		if(reply['type'] == 'text'):
			return reply_text(reply)
	else:
		return ''


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
		try:
			temp[x] = data[x]['#text']
		except Exception as  e:
			continue
	if temp['MsgType'] == 'text':
		temp['keyword'] = temp['Content']
	elif temp['MsgType'] == 'voice':
		if 'Recognition' in temp.keys():
			temp['keyword'] = temp['Recognition']
		else:
			temp['keyword'] = 'voice'
	elif temp['MsgType'] == 'event':
		if temp['Event'] =='CLICK':
			temp['keyword'] = temp['EventKey']
		else:
			temp['keyword'] = temp['Event']
	else:
		temp['keyword'] = temp['MsgType']
	global keyword,openid,token
	keyword = temp['keyword']
	openid = temp['FromUserName']
	token = temp['ToUserName']
	return temp
	
def reply_text(data):
	 extTpl = '''<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName>
	 <CreateTime>%s</CreateTime>
	 <MsgType><![CDATA[%s]]></MsgType>
	 <Content><![CDATA[%s]]></Content>
	 </xml>'''
	 try:
	 	extTpl = extTpl %(openid,token,
	 		str(int(time.time())),'text',data['Content'])
	 except Exception as e:
	 	return ''
	 return extTpl

def reply_pic(data):
	extTpl = '''<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%s</CreateTime>
	<MsgType><![CDATA[image]]></MsgType>
	<Image>
	<MediaId><![CDATA[%s]]></MediaId>
	</Image>
	</xml>'''
	try:
		extTpl  = extTpl % (openid,token,
			str(int(time.time())),data['MediaId'])
	except Exception as e:
		return ''
	return extTpl

def reply_voice(data):
	extTpl = '''<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%s</CreateTime>
	<MsgType><![CDATA[voice]]></MsgType>
	<Voice>
	<MediaId><![CDATA[%s]]></MediaId>
	</Voice>
	</xml>'''
	try:
		extTpl = extTpl % (openid,token,st(int(time.time())),data['MediaId'])
	except Exception as e:
		return ''
	return extTpl

def reply_vedio(data):
	extTpl = '''<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%s</CreateTime>
	<MsgType><![CDATA[video]]></MsgType>
	<Video>
	<MediaId><![CDATA[%s]]></MediaId>
	<Title><![CDATA[%s]]></Title>
	<Description><![CDATA[%s]]></Description>
	</Video> 
	</xml>'''
	try:
		extTpl = extTpl % (openid,token,
			str(int(time.time())),data['MediaId'],data['Title'],data['Description'])
	except Exception as e:
		return ''
	return extTpl

def reply_music(data):
	extTpl = '''<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%s</CreateTime>
	<MsgType><![CDATA[music]]></MsgType>
	<Music>
	<Title><![CDATA[%s]]></Title>
	<Description><![CDATA[%s]]></Description>
	<MusicUrl><![CDATA[%s]]></MusicUrl>
	</Music>
	</xml>'''
	try:
		extTpl = extTpl % (openid,token,str(int(time.time())),data['Title'],
			data['Description'],data['MusicUrl'])
	except Exception as e:
		return ''
	return extTpl

#def reply_