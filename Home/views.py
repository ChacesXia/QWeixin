from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from JwApi.Jw import OucJw
import json
# Create your views here.
def home_page(x):
	pass
def index(request):
	  oucjw = OucJw('13020031081', 'f01df23e7aee0050cd929fbf0f508d27');
	  oucjw.login()
	  return HttpResponse(json.dumps(oucjw.getCurrentCourseData()), content_type="application/json")  
def test(request):
	  return mHttpResponse("Hello, world. You're at the WeixinManage test")
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)