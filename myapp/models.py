from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUserModel(AbstractUser):

    phone_number = models.CharField(max_length=15, unique=True, blank=False)
    is_private = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    email = models.EmailField(unique=True, blank=False)

    def clean(self):
        super().clean()
        if self.username:
            self.username = self.username.lower()

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower()
        super().save(*args, **kwargs)

class FollowingModel(models.Model):

    following_id = models.ForeignKey(CustomUserModel,related_name="following", on_delete=models.CASCADE)

    user_obj = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)

class NotificationModel(models.Model):
    message = models.CharField(max_length=100,blank=False)
    sender = models.ForeignKey(CustomUserModel,related_name = "send_notification",on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUserModel,related_name="received_notification",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class FollowRequestModel(models.Model):
    sender = models.ForeignKey(CustomUserModel,related_name = "send_request",on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUserModel,related_name="received_request",on_delete=models.CASCADE)
    accept = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)