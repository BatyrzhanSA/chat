from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('chat/', views.chat, name='chat'),
    path('archive/', views.archive, name='archive'), 
]
