from django.conf.urls import url
from .views import *
urlpatterns =[
	url(r'^getScoreJSON',getScoreJSON),
	url(r'^index/(?P<id>.+)/',index,name = 'oucjwindex'),
	url(r'^bind/(?P<id>.+)/',bind,name = 'oucjwbind'),
	url(r'^detail/(?P<id>.+)/',detail,name = 'oucjwdetail'),
	url(r'^update/(?P<id>.+)/',updateScore,name = 'oucjwupdate'),
	url(r'^updatec/(?P<id>.+)/',getRecentCourse,name = 'oucjwupdatec'),
]