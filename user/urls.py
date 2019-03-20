from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from .forms import LoginForm

app_name = 'user'
urlpatterns = [
    path('signup/',
         SignUpView.as_view(),
         name='signup'),
    path('login/',
         auth_views.LoginView.as_view(
                 template_name='user/login.html',
                 authentication_form=LoginForm),
         name='login'),
    path('account/',
         AccountView.as_view(),
         name='account')
]
