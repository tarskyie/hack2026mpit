# news_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list', views.NewsListCreateView.as_view(), name='news-list'),
]
