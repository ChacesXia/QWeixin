from django.db import models

# Create your models here.
class Question(models.Model):
	question_text =  models.CharField(max_length = 150)
	pub_date = models.DateTimeField("pub_time")

	def __str__(self):
		return self.question_text

class Choice(models.Model):
	question =  models.ForeignKey(Question)
	choice_text = models.CharField(max_length = 200)
	votes = models.IntegerField(default = 0)