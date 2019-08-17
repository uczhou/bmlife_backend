from django.urls import include, path

urlpatterns = [
    path('location/', include('geolocation.urls')),
    path('info/', include('crimemap.urls')),
    path('rental/', include('rental.urls')),
]
