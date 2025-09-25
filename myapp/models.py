from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUserModel(AbstractUser):

    phone_number = models.CharField(max_length=15)

class FollowingModel(models.Model):

    following_id = models.ForeignKey(CustomUserModel,related_name="following", on_delete=models.CASCADE)

    user_obj = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)
