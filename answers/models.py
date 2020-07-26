from django.db import models
from questions.models import Question
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Answer(models.Model):
    body = models.TextField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="answers", null=True
    )

    def __str__(self):
        return self.body.split(".")[0]
