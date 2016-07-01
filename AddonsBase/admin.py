from django.contrib import admin
from .models import Addon,Keyword
# Register your models here.
class addonAdmin(admin.ModelAdmin):
	list_display = ['name','title','description','status']
	list_filter =['status']

class keywordAdmin(admin.ModelAdmin):
	list_display = ['keyword','addon','type','token']
	list_filter = ['type','token']
admin.site.register(Addon,addonAdmin)
admin.site.register(Keyword,keywordAdmin)