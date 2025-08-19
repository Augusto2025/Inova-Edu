from django.contrib import admin
from django.urls import path
from InovaEdu import views

urlpatterns = [
    path('', views.login),
    path('login.html', views.login, name='login'),
    path('test.html', views.home, name='home'),
]