from rest_framework_gis.pagination import GeoJsonPagination
from .serializers import *
from .models import *
from .filter import *
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response


class GeojsonStateLocation(generics.RetrieveUpdateAPIView):
    # -- other omitted view attributes --- #
    pagination_class = GeoJsonPagination
    queryset = State.objects.all()
    lookup_field = 'stusps'
    serializer_class = StateSerializer


class GeojsonUrbanAreaLocation(generics.RetrieveUpdateAPIView):
    # -- other omitted view attributes --- #
    pagination_class = GeoJsonPagination
    queryset = UrbanArea.objects.all()
    lookup_field = 'name10'
    serializer_class = UrbanAreaSerializer


class GeojsonCountyLocation(generics.RetrieveUpdateAPIView):
    # -- other omitted view attributes --- #
    pagination_class = GeoJsonPagination
    queryset = County.objects.all()
    lookup_field = 'pk'
    serializer_class = CountySerializer


class GeojsonZipCode(generics.RetrieveUpdateAPIView):
    # -- other omitted view attributes --- #
    pagination_class = GeoJsonPagination
    queryset = ZipCode.objects.all()
    lookup_field = 'zcta5ce10'
    serializer_class = ZipCodeSerializer


class ZipCodesWithin(generics.ListCreateAPIView):
    pagination_class = GeoJsonPagination
    queryset = ZipCode.objects.all()
    serializer_class = ZipCodeSerializer
    ploygon_filter_include_overlapping = True
    order_by = 'zcta5ce10'
    ploygon_filter_field = 'geom'

    filter_backends = (InPolygonFilter, OrderingFilter,)

    def get(self, request, *args, **kwargs):
        return Response('Invalid request.', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
