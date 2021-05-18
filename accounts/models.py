from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

    

class UserProfile(models.Model):
  user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
  slug = models.SlugField(max_length=100)
  cook_img = models.ImageField(null=True, blank=True)
  description = models.CharField(max_length=400, null=True)
  # like_recipe = models.ManyToManyField('Recipe', null=True,  related_name='favourite', blank=True)


  @property
  def get_photo_url(self):
      if self.cook_img and hasattr(self.cook_img, 'url'):
          return self.cook_img.url
      else:
          return "/static/images/anonym=user.png"

  def get_url(self):
      return reverse('accounts:user', args=[self.slug])


  # def add_like_recipe(self, idR):
  #   like_recipe.add(Recipe.objects.get(id=idR))
  
  def __str__(self):
    return self.user.username