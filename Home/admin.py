from django.contrib import admin

# Register your models here.
from .models import WeixinInfo,User
class WeixinInfoAdmin(admin.ModelAdmin):
	list_display = ['name','uid','type','originid','getcheckurl']
admin.site.register(WeixinInfo,WeixinInfoAdmin)
admin.site.register(User)