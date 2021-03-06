from django.db import models
from Home.models import WeixinInfo
# Create your models here.
type_choices = (
	('0','模糊'),
	('1','精确'),
	)
status_choices = (
	('0','关闭'),
	('1','开启'),
	)
class Addon(models.Model):
	name = models.CharField('标识',max_length = 200)
	title = models.CharField('中文名',max_length = 200)
	description = models.TextField('插件描述',)
	status = models.CharField('状态',choices = status_choices,max_length = 2)

	def __str__(self):
		return self.title


class Keyword(models.Model):
	keyword = models.CharField('关键词',max_length = 200)
	addon = models.ForeignKey(Addon)
	type = models.CharField('类别',max_length = 2,default = '0',choices = type_choices)
	token = models.ForeignKey(WeixinInfo)

	def __str__(self):
		return self.keyword
