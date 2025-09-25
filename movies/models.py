from django.db import models
from myapp.models import *

class WishlistModel(models.Model):

    user_id = models.OneToOneField(CustomUserModel,on_delete=models.CASCADE)

class WatchlistModel(models.Model):

    user_id = models.OneToOneField(CustomUserModel,on_delete=models.CASCADE)

class WatchlistItems(models.Model):

    watchlist_id = models.ForeignKey(WatchlistModel, on_delete=models.CASCADE)

    movie_id = models.CharField(max_length=100)

    title = models.CharField(max_length=100)

    poster_path = models.CharField(max_length=100, blank=True, null=True)

    created_date = models.DateField(auto_now_add=True)

    watch_status = models.BooleanField(default=False)

class WishlistItems(models.Model):

    wishlist_id = models.ForeignKey(WishlistModel,on_delete=models.CASCADE)

    movie_id = models.CharField(max_length=100)

    title = models.CharField(max_length=100)

    poster_path = models.CharField(max_length=100, blank=True, null=True)

    watch_id = models.BooleanField(default=False)

class ReviewModel(models.Model):

    user_id = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)

class ReviewItems(models.Model):

    review_id = models.ForeignKey(ReviewModel,on_delete=models.CASCADE)

    movie_id = models.CharField(max_length=100)

    poster_path = models.CharField(max_length=200,blank=True,null=True)

    title = models.CharField(max_length=100)

    rating = models.IntegerField()

    content = models.TextField()

    created_date = models.DateField(auto_now_add=True)

