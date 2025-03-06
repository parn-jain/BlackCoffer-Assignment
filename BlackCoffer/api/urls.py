from django.urls import path
from . import views

urlpatterns = [
    path('dataS/', views.DataListView.as_view(), name='data-list'),
    path('intensity-time/', views.intensity_time_api, name='intensity_time_api'),
    path('Intensity_Country/', views.Intensity_Country_api, name='Intensity_Country_api'),
    path('sunburst/', views.sunburst_chart, name='sunburst_chart')
]
