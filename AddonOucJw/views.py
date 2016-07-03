from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.db.models import Q
from django.conf import settings
import json
from .models import *
from JwApi.Jw import *
from .models import *
import re
# Create your views here.
msgdata = {}
openid = ''
token = ''
keyword = ''
username = ''
password = ''
def oucjwmain(request,data):
	global msgdata,openid,token,keyword,username,password
	msgdata = data
	openid = data['FromUserName']
	token = data['ToUserName']
	keyword = data['keyword']
	reply = {}
	if keyword == 'cj' or keyword == '成绩':
		try:
			d = StudentInfo.objects.get(openid = openid)
			username = d
		except Exception as e: # not bind jw
			reply['type'] = 'text'
			reply['Content'] = "您还没绑定!\n<a href ='" + settings.HOST+reverse('oucjwbind',args = (openid,))+"'>点我绑定教务系统</a>" 
			return reply
		try:
			return updateScore()
		except Exception as e:
			return 1

def  index(request,id):
	global openid,username
	openid = id
	request.session['openid'] = openid
	try:
		d = StudentInfo.objects.get(openid = openid)
		username = d
	except Exception as e:
		return HttpResponse(error())	
	if(request.method == 'GET'):
		context = {'openid':openid}
		data = getScoreInfo()
		return render(request, 'AddonOucJw/index.html', {'openid': openid,'data':data})
	else:
		return HttpResponse(json.dumps(getScoreInfo()),content_type="application/json")

def bind(request,id):
	global openid
	openid = id
	request.session['openid'] = openid
	if(request.method == 'GET'):
			return render(request, 'AddonOucJw/bind.html', {'openid': openid})
	else:
		return HttpResponse(bindpost(request),content_type="application/json")
def bindpost(request):
	global openid
	openid = request.POST.get('openid')
	username = request.POST.get('u1')
	password = request.POST.get('u2')
	email = request.POST.get('u4')
	try:
		d = StudentInfo.objects.get(openid = openid)
		result = {}
		result['status'] = -1
		result['message'] = '该微信号已绑定教务账号，请解绑' 
		return json.dumps(result)
	except Exception as e:
		try:
			oucjw = OucJw(username,password)
			result = oucjw.yz()
			if result['status'] == '200':		
				d = StudentInfo(username = username,password = password,mail = email,openid = openid)
				d.save()
				result = {}
				result['status'] = 200
				result['message'] = '绑定成功'
				return json.dumps(result)
			else:
				return json.dumps(result)
		except Exception as e:
			result = {}
			result['status'] = -2
			result['message'] = '绑定失败，请联系管理员'
			return json.dumps(result)

def updateScore(request,id):
	global openid,username
	openid = id
	try:
		username = StudentInfo.objects.get(openid = openid)
		return HttpResponse(upScore(),content_type="application/json")
	except Exception as e:
		return HttpResponse(error(),content_type="application/json")


def detail(request,id):
	global openid
	openid = request.POST.get('openid')
	year =  request.POST.get('year')
	request.session['openid'] = openid
	
def getScoreInfo():
	d = StudentScore.objects.filter(username = username).order_by('-year')
	xqdata = []
	tempyear = ''
	totalxf = 0;totaljd = 0;count = 0;total  = 0;totalxf1 = 0;gk =0;jdxf = 0
	for x in d:
		if tempyear == '':
			tempyear = x.year
			if tempyear.endswith('0'):
				xq = tempyear[:-1] +"夏"
			elif tempyear.endswith('1'):
				xq = tempyear[:-1] + "秋"
			else:
				xq = str(int(tempyear[:-1])+1) + "春"
			temp = [{'coursename':fun(x.coursename),'coursetype':x.coursetype,
				'xf':x.xf,'coursescore':x.score}]
		elif tempyear != x.year:
			xqdata.append({xq:temp})
			temp = []
			tempyear = x.year
			if tempyear.endswith('0'):
				xq = tempyear[:-1] +"夏"
			elif tempyear.endswith('1'):
				xq = tempyear[:-1] + "秋"
			else:
				xq = str(int(tempyear[:-1])+1) + "春"
			temp = [{'coursename':fun(x.coursename),'coursetype':x.coursetype,'xf':x.xf,'coursescore':x.score}]
		else:
			temp.append({'coursename':fun(x.coursename),'coursetype':x.coursetype,'xf':x.xf,'coursescore':x.score})
		totalxf += x.xf
		totaljd += x.jd * x.xf
		if x.jd != 0:
			jdxf += x.xf
		count += 1
		try:
			t = float(x.score)
			total += t * x.xf
			totalxf1 += x.xf
			if(t < 60):
				gk += 1
				totaljd-= x.jd*x.xf
				totalxf -=x.xf
				total -= t * x.xf
				totalxf1 -=x.xf
		except Exception as e:
			continue
	xqdata.append({xq:temp})
	#xqdata = sorted(xqdata.items(), key=lambda d:d[0]) 
	all = {'gk':gk,'total':totalxf,'jd':round(totaljd/jdxf,2),'km':count,'jq':round(total / totalxf1,2)}
	data = {'status':'200','all':all,'xqdata':xqdata}
	return (data)

def getScoreData(year = ''):
	if(year == ''):
		d = StudentScore.objects.filter(Q(username = username) 
			&(Q(year = 20151) | Q(year = 20152)))
	else:
		d = StudentScore.objects.filter(Q(username  = username) & Q(year = year))
	data = []
	temp = {}
	for x in d:
		temp['coursename'] = x.coursename
		temp['coursetype'] = x.coursetype
		temp['year'] = x.year
		temp['score'] = x.score
		temp['jd'] = x.jd
		temp['xf'] = x.xf
		data.append(temp)
	return data

def getScoreJSON(request):
	global openid,username
	openid = request.POST.get('openid')
	year = request.POST.get('year')
	try:
		d = StudentInfo.objects.get(openid = openid)
		username = d
	except Exception as e:
		return HttpResponse(error())
	if year =='':
		scoredata = getScoreData()
	else:
		scoredata = getScoreData(year)
	result = {}
	result['status'] = 200
	result['message'] ='数据获取成功'
	result['data'] = scoredata
	return HttpResponse(json.dumps(result))

def upScore():
	oucjw = OucJw(username.username,username.password)
	data = oucjw.login()
	if data['status'] == '200':
		try:
			tscoredata = oucjw.getScoreData()
			scoredata = StudentScore.objects.filter(username = username)
			if len(scoredata) == len(tscoredata):
				pass
			else:
				
				for x in scoredata:
					del tscoredata[x.coursename+x.year]
				for (k,x) in tscoredata.items():
					temp = StudentScore(username = username,coursename = x['coursename'],
						coursetype = x['coursetype'],year=x['year'],jd=x['jd'],score=x['score'],xf=x['xf'])
					temp.save()
			data = {}
			data['status'] = 200
			data['message'] = '更新成功'
			data['data'] = tscoredata
		except Exception as err:
			return(err)
			data = {}
			data['status'] = -1
			data['message'] = '更新失败'
	return json.dumps(data)

def error():
	result = {}
	result['status'] = '301'
	result['message'] = '数据获取失败'
	return json.dumps(result)
def fun(s):
    return re.sub(r'([\d]+|\[|\])','',s).lower()