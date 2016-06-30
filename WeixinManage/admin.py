from django.contrib import admin

# Register your models here.
from .models import Question,Choice

class ChoiceInline(admin.StackedInline):
	model = Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	fields = ['pub_date','question_text']
	list_display = ('question_text','pub_date')
	list_filter = ['pub_date']
	inlines = [ChoiceInline]

admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)