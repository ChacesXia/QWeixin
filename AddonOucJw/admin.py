from django.contrib import admin
from .models import *
class StudentAdmin(admin.ModelAdmin):
	list_display = ['username','password','mail','openid','token']
	search_fields = ['username','mail']
class ScoreAdmin(admin.ModelAdmin):
	list_display = ['username','coursename','coursetype','year','score','xf']
	search_fields = ['coursename']
	list_filter = ['year']
class CourseAdmin(admin.ModelAdmin):
	list_display = ['username','coursename','year','teacher','xkh','xkb','xf']
	list_filter = ['year']

admin.site.register(StudentInfo,StudentAdmin)
admin.site.register(StudentScore,ScoreAdmin)
admin.site.register(StudentCourse,CourseAdmin)