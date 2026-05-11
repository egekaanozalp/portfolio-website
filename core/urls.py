from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("portfolio/<slug:slug>/", views.portfolio_detail, name="portfolio_detail"),
]
