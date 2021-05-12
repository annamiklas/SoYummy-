from django.db import models

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
  name = models.CharField(max_length=200, null=True)
  recipe_img = models.ImageField(null=True, blank=True)
  ingredients = models.TextField(max_length=1000, null=True)
  category = models.ManyToManyField(Category)
  description = models.TextField(max_length=1000, null=True)
  preparation_time = models.CharField(max_length=10, blank=True, null=True)
  level = models.CharField(max_length=30, null=True, choices=LEVEL)
  data_created = models.DateTimeField(auto_now_add=True)

  @property
  def get_photo_url(self):
      if self.recipe_img and hasattr(self.recipe_img, 'url'):
          return self.recipe_img.url
      else:
          return "/static/images/pesto.jpg"

  def __str__(self):
    return self.name
