from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("category/<int:category_id>", views.category_listings, name="category_listings"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("past_listings", views.past_listings, name="past_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist")
]
