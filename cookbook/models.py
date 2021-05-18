from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.db.models import Avg, Count

from category.models import Category
from accounts.models import UserProfile

# Create your models here.



class Recipe(models.Model):
  LEVEL = (
    ('Easy','Easy'),
    ('Medium','Medium'),
    ('Hard','Hard'),
  )
  cook = models.ForeignKey(UserProfile, null=True, blank=True,  related_name='creator', on_delete=models.SET_NULL)
  name = models.CharField(max_length=200)
  recipe_img = models.ImageField(null=True, blank=True)
  ingredients = models.TextField(max_length=1000, null=True)
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

  def averageReview(self):
      reviews = Rating.objects.filter(recipe=self).aggregate(average=Avg('rating'))
      avg = 0
      if reviews['average'] is not None:
          avg = float(reviews['average'])
      return avg

  def countReview(self):
      reviews = Rating.objects.filter(recipe=self).aggregate(count=Count('id'))
      count = 0
      if reviews['count'] is not None:
          count = int(reviews['count'])
      return count


class Ingredient(models.Model):
  recipe = ForeignKey(Recipe, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  amount = models.DecimalField(max_digits=5, decimal_places=1)
  unit = models.CharField(max_length=30)

class Rating(models.Model):
  recipe = models.ForeignKey(Recipe, on_delete=CASCADE)
  user = models.ForeignKey(UserProfile, on_delete=CASCADE)
  rating = models.FloatField()
  creation_date = models.DateTimeField(auto_now_add=True)