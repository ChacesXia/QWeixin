from django.shortcuts import render
from django.template import RequestContext 
from django.http import HttpResponse
from Home.models import WeixinInfo
from .wechat import reply_main
import time
import hashlib 
# Create your views here.
def index(request,id):
	if(request.method == 'GET'):
		try:
			response =   HttpResponse(checkSignature(request,id), content_type="text/plain")
		except Exception as e:
			return HttpResponse('Request failed')
		return response
	else:
		return HttpResponse(reply_main(request,request.body,id))

def checkSignature(request,id):
	weixindata = WeixinInfo.objects.get(id = id)
	signature = request.GET.get("signature", None)
	timestamp = request.GET.get("timestamp", None)
	nonce = request.GET.get("nonce", None)
	echoStr = request.GET.get("echostr",None)
	token = weixindata.token
	tmpList = [token,timestamp,nonce]
	tmpList.sort()
	tmpstr = ("%s%s%s" % tuple(tmpList)).encode(encoding ='gbk')
	tmpstr = hashlib.sha1(tmpstr).hexdigest()
	if tmpstr == signature:
		return echoStr
	else:
		return None

