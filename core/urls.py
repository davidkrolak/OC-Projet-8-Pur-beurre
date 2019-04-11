from django.urls import path

from .views import *

app_name = 'core'
urlpatterns = [
    path('',
         HomeView.as_view(),
         name='home'),
    path('research/',
         ResearchView.as_view(),
         name='research'),
    path('substitute/<int:id>',
         SubstituteView.as_view(),
         name='substitute'),
    path('product/<int:id>',
         ProductView.as_view(),
         name='product')

]
