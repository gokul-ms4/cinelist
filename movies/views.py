from django.shortcuts import render,redirect

from django.views.generic import View

from .tmdb_client import get_popular_movies, search_movies

from movies.models import *

from movies.forms import *

import requests

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

API_KEY = 'faecc784db46297338de9a2cec3b7cc2'

BASE_URL = 'https://api.themoviedb.org/3'

class MovieListView(View):
 
 def get(self,request):

    query = request.GET.get("query")

    if query:

        movies = search_movies(query)

    else:

        movies = get_popular_movies()

    return render(request, "movie_list.html", {"movies": movies})

@method_decorator(login_required,name="dispatch")
class MovieDetailView(View):
   
   def get(self,request,**kwargs):
      
       id = kwargs.get("id")

       movie_response = requests.get(
          url=f"{BASE_URL}/movie/{id}",
          params={"api_key" : API_KEY}
       )

       movie = movie_response.json()

       crew_response = requests.get(
          url=f"{BASE_URL}/movie/{id}/credits",
          params={"api_key" : API_KEY}
       )

       cast = crew_response.json()

       watchlist = WatchlistModel.objects.get(user_id = request.user)

       wishlist = WishlistModel.objects.get(user_id = request.user)

       is_watchlist = WatchlistItems.objects.filter(watchlist_id = watchlist, movie_id = id)

       is_wishlist = WishlistItems.objects.filter(wishlist_id = wishlist,movie_id = id)

       return render(request,"movie_detail.html",{"movie":movie,"cast":cast, "is_watchlist" : is_watchlist, "is_wishlist" : is_wishlist})

class About(View):

   def get(self,request):

      return render(request,"about.html")

@method_decorator(login_required,name="dispatch")   
class WatchlistAddView(View):

   def post(self,request,**kwargs):

         id = kwargs.get("id")

         user = WatchlistModel.objects.get(user_id = request.user)

         response = requests.get(
            url=f"{BASE_URL}/movie/{id}",
            params={"api_key" : API_KEY}
         )

         data = response.json()

         WatchlistItems.objects.create(watchlist_id = user, movie_id = id, title = data.get("title"), poster_path = data.get("poster_path"))

         return redirect("movie_detail",id)

@method_decorator(login_required,name="dispatch")   
class WatchlistItemsView(View):

   def get(self,request):

      user = request.user

      watchlist_id = WatchlistModel.objects.get(user_id = user)

      watchlist = WatchlistItems.objects.filter(watchlist_id = watchlist_id)

      review_id = ReviewModel.objects.get(user_id = request.user)

      movie_list = []

      for i in watchlist:

         movie_id = i.movie_id

         review_item = ReviewItems.objects.filter(review_id = review_id, movie_id = movie_id)

         if review_item:

            is_review = True

         else:

            is_review = False

         movie_list.append({
            "movie_id" : i.movie_id,
            "title" : i.title,
            "poster_path" : i.poster_path,
            "created_date" : i.created_date,
            "watch_status" : i.watch_status,
            "is_review" : is_review
         })

      return render(request,"user_watchlist.html",{"movie_list" : movie_list})

@method_decorator(login_required,name="dispatch") 
class WatchlistDeleteView(View):

   def get(self,request,**kwargs):

      id = kwargs.get("id")

      watchlist = WatchlistModel.objects.get(user_id = request.user)

      WatchlistItems.objects.get(watchlist_id = watchlist, movie_id = id).delete()

      return redirect("user_watchlist")

@method_decorator(login_required,name="dispatch")  
class WatchlistUpdateView(View):

   def get(self,request,**kwargs):

      id = kwargs.get("id")

      watchlist = WatchlistModel.objects.get(user_id = request.user)

      item = WatchlistItems.objects.get(watchlist_id = watchlist, movie_id = id)

      item.watch_status = True

      item.save()

      return redirect("user_watchlist")

@method_decorator(login_required,name="dispatch") 
class wishlistAddView(View):

   def post(self,request,**kwargs):

      id = kwargs.get("id")

      response = requests.get(
         url=f"{BASE_URL}/movie/{id}",
         params={"api_key" : API_KEY}
      )

      data =response.json()

      wishlist = WishlistModel.objects.get(user_id = request.user)

      WishlistItems.objects.create(wishlist_id = wishlist, movie_id = id, title = data.get("title"), poster_path = data.get("poster_path"))

      return redirect("movie_detail",id)
   
@method_decorator(login_required,name="dispatch")
class WishlistItemsView(View):

   def get(self,request):

      wishlist_id = WishlistModel.objects.get(user_id = request.user)

      wishlist = WishlistItems.objects.filter(wishlist_id=wishlist_id)

      watchlist_id = WatchlistModel.objects.get(user_id = request.user)

      for i in wishlist:

         movie_id = i.movie_id

         watchlist = WatchlistItems.objects.filter(watchlist_id = watchlist_id, movie_id = movie_id)

         if watchlist:

            item = WishlistItems.objects.get(wishlist_id = wishlist_id, movie_id= movie_id)

            item.watch_id = True

            item.save()

         else:

            item = WishlistItems.objects.get(wishlist_id = wishlist_id, movie_id= movie_id)

            item.watch_id = False

            item.save()

      movie_list = WishlistItems.objects.filter(wishlist_id=wishlist_id)

      return render(request,"user_wishlist.html", {"movie_list" : movie_list})

@method_decorator(login_required,name="dispatch") 
class WishlistDeleteView(View):

   def get(self,request,**kwargs):

      id = kwargs.get("id")

      wishlist_id = WishlistModel.objects.get(user_id = request.user)

      WishlistItems.objects.get(wishlist_id = wishlist_id, movie_id = id).delete()

      return redirect("user_wishlist")

@method_decorator(login_required,name="dispatch") 
class WishlistToWatchlistView(View):

   def get(self,request,**kwargs):

      id = kwargs.get("id")

      watchlist_id = WatchlistModel.objects.get(user_id = request.user)

      wishlist_id = WishlistModel.objects.get(user_id = request.user)

      wishlist = WishlistItems.objects.get(wishlist_id = wishlist_id, movie_id = id)

      title = wishlist.title

      poster_path = wishlist.poster_path

      WatchlistItems.objects.create(watchlist_id = watchlist_id, movie_id = id, title = title, poster_path = poster_path)

      return redirect("user_wishlist")

class CinelistHomeView(View):

   def get(self,request):

      return render(request, "cinelist_home.html")
   
class ReviewAddView(View):

   def get(self,request,**kwargs):

      id = kwargs.get("id")

      request.session["id"] = id

      form = ReviewForm

      watchlist_id = WatchlistModel.objects.get(user_id = request.user)

      title = WatchlistItems.objects.get(watchlist_id = watchlist_id,movie_id = id)

      return render(request,"review_form.html",{"form" : form , "title" : title.title})

   def post(self,request,**kwargs):

      id = kwargs.get("id")

      form = ReviewForm(request.POST)

      watchlist_id = WatchlistModel.objects.get(user_id = request.user)

      watchlist = WatchlistItems.objects.get(watchlist_id = watchlist_id, movie_id = id)

      review = ReviewModel.objects.get(user_id = request.user)

      if form.is_valid():

        rating =  form.cleaned_data.get("rating")

        content = form.cleaned_data.get("content")

        title = watchlist.title

        poster_path = watchlist.poster_path

        movie_id = id

        review_id = review

        ReviewItems.objects.create(rating = rating, content = content, title = title, poster_path = poster_path, movie_id = movie_id, review_id = review_id)

        return redirect("user_reviews")

class ReviewUpdateView(View):

   def get(self,request,**kwargs):

      id = kwargs.get("id")

      review_id = ReviewModel.objects.get(user_id = request.user)

      review_item = ReviewItems.objects.get(review_id = review_id, movie_id = id)

      form = ReviewForm(instance=review_item)

      return render(request,"review_update.html",{"form" : form, "title" : review_item.title})
   
   def post(self,request,**kwargs):

      id = kwargs.get("id")

      review_id = ReviewModel.objects.get(user_id = request.user)

      review_item = ReviewItems.objects.get(review_id = review_id, movie_id = id)

      form = ReviewForm(request.POST, instance=review_item)

      if form.is_valid():

         form.save()

      return redirect("user_reviews")
   
class ReviewDeleteView(View):

   def get(self,request,**kwargs):

      id = kwargs.get("id")

      review_id = ReviewModel.objects.get(user_id = request.user)

      ReviewItems.objects.get(review_id = review_id, movie_id = id).delete()

      return redirect("user_reviews")
   
@method_decorator(login_required,name="dispatch")  
class UserReviewsView(View):

   def get(self,request):

      review_id = ReviewModel.objects.get(user_id = request.user)

      reviews = ReviewItems.objects.filter(review_id = review_id)

      range_obj = range(1,6)

      return render(request,"user_reviews.html",{"reviews" : reviews,"range" : range_obj})

class MovieReviewsView(View):

   def get(self,request,**kwargs):

      id = kwargs.get("id")

      user = request.user

      reviews = ReviewItems.objects.filter(movie_id = id)

      if reviews:

       for i in reviews:

         title = i.title

         break
       
      else:

         title = ""

      range_obj = range(1,6)
      
      users = [user.username,"admin"]

      print(users)
   
      return render(request,"movie_reviews.html",{"reviews":reviews, "range" : range_obj, "title" : title, "users" : users})
   
class OtherWatchlistView(View):

   def get(self,request,**kwargs):

      user_id = kwargs.get("id")

      name = CustomUserModel.objects.get(id = user_id)

      watchlist_id = WatchlistModel.objects.get(user_id = user_id)

      Watchlist = WatchlistItems.objects.filter(watchlist_id=watchlist_id, watch_status =True)

      return render(request,"other_watchlist.html",{"watchlist" : Watchlist, "name" : name.username})
   
class OtherReviewView(View):

   def get(self,request,**kwargs):

      user_id = kwargs.get("id")

      name = CustomUserModel.objects.get(id = user_id)

      review_id = ReviewModel.objects.get(user_id = user_id)

      reviews = ReviewItems.objects.filter(review_id = review_id)

      range_obj = range(1,6)

      return render(request,"other_reviews.html",{"reviews" : reviews, "range" : range_obj, "name" : name.username})