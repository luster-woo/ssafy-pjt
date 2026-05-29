from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:pk>', views.detail, name ='detail'),
    path('delete/<int:pk>/', views.delete, name ='delete'),
    path('update/<int:pk>/', views.update, name ='update'),
    path('create/', views.create, name ='create'),
]
