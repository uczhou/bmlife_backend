from django.urls import path
from . import views

urlpatterns = [
    path('house/', views.BMHouseListView.as_view()),
    path('house/<str:uuid>', views.BMHouseView.as_view()),
    path('location/', views.HouseLocationListView.as_view()),
    path('house/polygon/', views.BMHouseInPolygonListView.as_view()),
]