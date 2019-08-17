from django.urls import path
from . import views

urlpatterns = [
    path('crime/<slug:state>/', views.CrimeListView.as_view()),
]