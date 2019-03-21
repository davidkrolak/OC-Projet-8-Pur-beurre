from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'user'
urlpatterns = [
    path('signup/',
         SignUpView.as_view(),
         name='signup'),
    path('login/',
         ConnectionView.as_view(),
         name='login'),
    path('logout/',
         DisconnectionView.as_view(),
         name='logout'),
    path('account/',
         AccountView.as_view(),
         name='account')
]
