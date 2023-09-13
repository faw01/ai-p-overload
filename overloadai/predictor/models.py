from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    volume = models.FloatField()
    reps = models.IntegerField()
    seconds = models.IntegerField()
    predicted_weight = models.FloatField()
    actual_weight = models.FloatField()
    feedback = models.IntegerField(choices=[(-1, 'Too light'), (0, 'Just right'), (1, 'Too heavy')])

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    exercise = models.CharField(max_length=100)
    weight = models.FloatField()
    sets = models.IntegerField()
    reps_per_set = models.IntegerField()
