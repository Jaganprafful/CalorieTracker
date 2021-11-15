from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    fullName = models.CharField(max_length=50, default=' ', null=True, blank=True)
    is_Client = models.BooleanField(default=False)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)


class Food(models.Model):
    name = models.CharField(max_length=100)
    carbs = models.FloatField()
    protein = models.FloatField()
    fats = models.FloatField()
    calories = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Profile(models.Model):
    relatedClient = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    totalCarbs = models.FloatField(default=0, null=True)
    totalProteins = models.FloatField(default=0, null=True)
    totalFats = models.FloatField(default=0, null=True)
    totalCalorie = models.FloatField(default=0, null=True)
    dateCreated = models.DateField(auto_now_add=True)
    caloriesGoal = models.PositiveIntegerField(default=0)


class ConsumedFood(models.Model):
    relatedFood = models.ForeignKey(Food, null=False, blank=False, on_delete=models.CASCADE)
    relatedClient = models.ForeignKey(Client, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    dateCreated = models.DateField(auto_now_add=True)

