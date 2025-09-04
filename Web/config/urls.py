from django.contrib import admin
from django.urls import path, include
from InovaEdu import views

urlpatterns = [
    path("", include("InovaEdu.urls"))
]