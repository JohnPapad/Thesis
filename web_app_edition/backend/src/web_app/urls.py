# chat/urls.py
from django.urls import path

from . import views as vs
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('users/signup', vs.UserCreate.as_view(),name='user-signup'),
    path('users/signin', vs.UserLogin.as_view(),name='user-signin'),
    path('lboard/nmm', vs.LeaderboardViews.NMM_Leaderboard.as_view(),name='user-lboard'),
]