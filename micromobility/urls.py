from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.homepageView, name="homepage"),  # type: ignore
    path("register/", view=views.registerView, name="register"),  # type: ignore
    path("logout/", view=views.logoutView, name="logout"),
    path("profiles/<str:username>/", view=views.profileView, name="profiles"),
    path(
        "profiles/<str:username>/watchlist", view=views.watchlistView, name="watchlist"
    ),
    path("auction/<int:pk>/", view=views.auctionDetailView, name="details"),
    path("watchlist_delete/<int:pk>/", view=views.deleteFromWatchList, name="delete"),
    path("watchlist_add/<int:pk>/", view=views.addInWatchList, name="add"),
    path("auctionNew/", view=views.auctionNew, name="auctionNew"),
]
