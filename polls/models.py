from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=100)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.text

    def was_published_recently(self):
        return (timezone.now() - timezone.timedelta(days=1)).date() <= self.pub_date <= timezone.now().date()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.text} :{self.votes}'
