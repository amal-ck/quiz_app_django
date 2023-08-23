from django.db import models
from quiz_master.models import QuizModel
from django.contrib.auth.models import User

class Results(models.Model):
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    quiz_user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_answers = models.PositiveIntegerField(null=True)
    incorrect_answers = models.PositiveIntegerField(null=True)
    skipped_answers = models.PositiveIntegerField(null=True)
    total_time_taken = models.FloatField(null=True)
