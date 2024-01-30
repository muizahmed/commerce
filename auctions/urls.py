from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("categories", views.categories_list, name="categories-list"),
    path("categories/<str:category>", views.category_view, name="category-view"),
    path("new-listing", views.new_listing, name="new-listing"),
    path("listing/<int:id>/<str:url>", views.listing, name="listing"),
    path("listing/<int:id>/<str:url>/bid", views.listing, name="bidding"),
    path("listing/<int:id>/<str:url>/watchlist", views.watchlist, name="add-to-watchlist"),
    path("listing/<int:id>/<str:url>/close", views.close_auction, name="close-auction"),
    path("comment/<int:id>/<str:url>", views.comment, name="comment"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
