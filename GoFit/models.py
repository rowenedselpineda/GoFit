from django.db import models
from django.contrib.auth.models import User


class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.fitness_class.name}"
