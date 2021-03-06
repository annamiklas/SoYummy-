from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    User._meta.get_field('email')._unique = True
    user_img = models.ImageField(null=True, blank=True)
    description = models.TextField(max_length=400, null=True)

    @property
    def get_photo_url(self):
        if self.user_img and hasattr(self.user_img, 'url'):
            return self.user_img.url
        else:
            return "/static/images/anonym=user.png"


    def __str__(self):
        return self.user.username
