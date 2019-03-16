from django.urls import path
from django.contrib.auth.models import auth
from user import views

urlpatterns = [
    path('signup/',
         views.signup,
         name='signup'),
    path('account_activation_sent/',
         views.account_activation_sent,
         name='account_activation_sent'),
    path('activate/<uidb64>/<token>',
         views.activate,
         name='activate')
]
