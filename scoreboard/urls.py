# scoreboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('scoreboard/', views.scoreboard, name='scoreboard'),
    path('challenges/', views.challenges, name='challenges'),
    path('challenge/<int:challenge_id>/', views.challenge_download, name='challenge_download'),
]