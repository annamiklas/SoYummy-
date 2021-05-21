from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.db.models import Avg, Count

from category.models import Category
from accounts.models import UserProfile


class Recipe(models.Model):
    LEVEL = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )
    cook = models.ForeignKey(UserProfile, null=True, blank=True, related_name='creator', on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    recipe_img = models.ImageField(null=True, blank=True)
    category = models.ManyToManyField(Category)
    description = models.TextField(max_length=1000, null=True)
    preparation_time = models.FloatField(blank=True, null=True)
    level = models.CharField(max_length=30, null=True, choices=LEVEL)
    creation_date = models.DateTimeField(auto_now_add=True)

    @property
    def get_photo_url(self):
        if self.recipe_img and hasattr(self.recipe_img, 'url'):
            return self.recipe_img.url
        else:
            return "/static/images/pesto.jpg"

    def __str__(self):
        return self.name

    def average_rating(self):
        rating = Rating.objects.filter(recipe=self).aggregate(average=Avg('rating'))
        avg = 0
        if rating['average']:
            avg = float(rating['average'])
        return avg

    def count_rating(self):
        rating = Rating.objects.filter(recipe=self).aggregate(count=Count('id'))
        count = 0
        if rating['count']:
            count = int(rating['count'])
        return count


class Ingredient(models.Model):
    recipe = ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    measurement = models.CharField(max_length=30, blank=True, null=True)


class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=CASCADE)
    rating = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True)
