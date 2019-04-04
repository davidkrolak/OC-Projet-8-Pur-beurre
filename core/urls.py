from django.urls import path

from .views import *

app_name = 'core'
urlpatterns = [
    path('',
         HomeView.as_view(),
         name='home'),
    path('research/',
         ResearchView.as_view(),
         name='research')
]