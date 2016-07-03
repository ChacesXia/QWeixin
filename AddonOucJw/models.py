from django.db import models
from Home.models import WeixinInfo
# Create your models here.
class StudentInfo(models.Model):
	username = models.CharField('username',max_length = 30)
	password = models.CharField('password',max_length = 120)
	mail = models.EmailField('email',max_length = 120)
	openid = models.CharField('openid',max_length = 120)
	token = models.ForeignKey(WeixinInfo,null = True)
	def __str__(self):
		return self.username

class StudentScore(models.Model):
	username = models.ForeignKey(StudentInfo)
	coursename = models.CharField('课程名',max_length = 200)
	coursetype = models.CharField('课程类型',max_length = 50)
	year = models.CharField('学年',max_length = 10)
	score = models.CharField('成绩',max_length = 40)
	jd = models.FloatField('绩点')
	xf = models.FloatField('学分')

	def __str__(self):
		return self.coursename + ' '+ self.score

class StudentCourse(models.Model):
	username = models.ForeignKey(StudentInfo)
	coursename = models.CharField('课程名',max_length = 200)
	xkh = models.CharField('选课号',max_length = 50)
	xkb = models.CharField('选课币',max_length = 10)
	year = models.CharField('学年',max_length = 10)
	xf = models.FloatField('学分')
	teacher = models.CharField('任课老师',max_length = 100)
