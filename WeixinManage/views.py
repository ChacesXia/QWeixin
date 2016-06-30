from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home_page(x):
	pass
def index(request):
	  return HttpResponse("Hello, world. You're at the WeixinManage index.")
    