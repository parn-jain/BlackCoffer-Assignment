from django.urls import path
from . import views

urlpatterns = [
    path('dataS/', views.DataListView.as_view(), name='data-list'),
    path('intensity-time/', views.intensity_time_api, name='intensity_time_api'),
    path('Intensity_Country/', views.Intensity_Country_api, name='Intensity_Country_api'),
    path('sunburst/', views.sunburst_chart, name='sunburst_chart'),
    path('get_unique_sectors/', views.get_unique_sectors, name='get_unique_sectors'),
    path('get_unique_countries/', views.get_unique_countries, name='get_unique_countries'),
    path('heatmap_sector_relevance_api/', views.heatmap_sector_relevance_api, name='heatmap_sector_relevance_api'),
]
