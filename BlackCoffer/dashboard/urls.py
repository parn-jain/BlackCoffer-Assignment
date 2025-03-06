from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path('datafead/', views.data, name = "data"),
    # path('intensity_time/', views.intensity_time, name = "intensity_time"),
    
]
