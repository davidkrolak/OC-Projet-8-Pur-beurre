from django.urls import path
from django.contrib.auth import views as auth_views
from user import views
from .forms import LoginForm

app_name = 'user'
urlpatterns = [
    path('signup/',
         views.signup,
         name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='user/login.html',
        authentication_form=LoginForm), name='login'),
]
