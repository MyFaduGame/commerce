from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("detail/<int:listing_id>", views.detail_view, name="detail_view"),
    path("detail/<int:listing_id>/bid", views.bid, name="bid"),
    path("detail/<int:listing_id>/bid_closed", views.close_bid, name="close_bid"),
    path("detail/<int:listing_id>/watchlist", views.watchlist, name="watchlist"),
    path("view_list", views.view_list, name="view_list")
    
    
]
