from django.urls import path
from movies.views import *

urlpatterns = [

    path('movie_list/',MovieListView.as_view(), name="movie_list"),
    path("movie_detail/<int:id>/",MovieDetailView.as_view(), name="movie_detail"),
    path("about/",About.as_view(),name="about"),
    path("watchlist_add/<int:id>/",WatchlistAddView.as_view(),name="watchlist_add"),
    path("wishlist_add/<int:id>/",wishlistAddView.as_view(),name="wishlist_add"),
    path("user_watchlist/",WatchlistItemsView.as_view(),name="user_watchlist"),
    path("watchlist_delete/<int:id>/",WatchlistDeleteView.as_view(),name="watchlist_delete"),
    path("watchlist_update/<int:id>",WatchlistUpdateView.as_view(),name="watchlist_update"),
    path("user_wishlist/",WishlistItemsView.as_view(), name="user_wishlist"),
    path("wishlist_delete/<int:id>/",WishlistDeleteView.as_view(),name="wishlist_delete"),
    path("wishlist_to_watchlist/<int:id>/", WishlistToWatchlistView.as_view(), name="wishlist_to_watchlist"),
    path("cinelist_home/",CinelistHomeView.as_view(), name="cinelist_home"),
    path("review_form/<int:id>/",ReviewAddView.as_view(), name="review_form"),
    path("review_update/<int:id>/",ReviewUpdateView.as_view(), name="review_update"),
    path("review_delete/<int:id>/",ReviewDeleteView.as_view(), name="review_delete"),
    path("user_reviews/",UserReviewsView.as_view(), name="user_reviews"),
    path("movie_reviews/<int:id>/",MovieReviewsView.as_view(), name="movie_reviews"),
    path("other_watchlist/<int:id>/",OtherWatchlistView.as_view(), name="other_watchlist"),
    path("other_reviews/<int:id>/",OtherReviewView.as_view(), name="other_reviews")

]