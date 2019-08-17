from django.urls import path
from . import views

urlpatterns = [
    path('state/<str:stusps>', views.GeojsonStateLocation.as_view()),
    path('urbanarea/<str:name10>', views.GeojsonUrbanAreaLocation.as_view()),
    path('county/<int:pk>', views.GeojsonCountyLocation.as_view()),
    path('zipcode/<str:zcta5ce10>', views.GeojsonZipCode.as_view()),
    path('zipcode/areas/', views.ZipCodesWithin.as_view()),
]