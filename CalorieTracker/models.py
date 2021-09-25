from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    fullName = models.CharField(max_length=50, default=' ', null=True, blank=True)


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    weight = models.FloatField()
    height = models.FloatField()
    phone = models.CharField(max_length=15, default='(000)000-0000')

    def __str__(self):
        return self.user.fullName

    def get_absolute_url(self):
        return reverse('client_detail', args=[str(self.id)])


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
