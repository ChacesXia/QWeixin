from django.contrib import admin

# Register your models here.
from .models import WeixinInfo,User
admin.site.register(WeixinInfo)
admin.site.register(User)