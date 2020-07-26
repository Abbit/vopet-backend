from django.db import models
from subjects.models import Subject


# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=64)
    body = models.TextField()
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="questions"
    )

    def __str__(self):
        return self.title
