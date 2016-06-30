from django.db import models

# Create your models here.
class User(models.Model):
	username  = models.CharField('用户名',max_length =  100)
	password = models.CharField('密码',max_length = 100)
	email = models.EmailField('邮箱',max_length = 100)
	register_time = models.DateTimeField('注册时间')
	last_login_time = models.DateTimeField('最后登陆时间')

class WeixinInfo(models.Model):
	type_choices = (
		('0','订阅号'),
		('1','服务号'),
		('2','企业号'),
		)
	weixinid = models.CharField('微信号',max_length = 200)
	name = models.CharField('微信名',max_length = 200)
	originid = models.CharField('原始id',max_length = 200) 
	appid = models.CharField('Appid',max_length  = 200)
	appkey = models.CharField('Appkey',max_length = 200)
	token = models.CharField(max_length = 100,default = 'qweixin')
	type = models.CharField('类型',choices = type_choices,default = '0',max_length = 2)
	uid = models.ForeignKey(User)


	


