from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_gis.filters import InBBoxFilter, DistanceToPointFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filter import InPolygonFilter, HouseFilter
from .house_serializer import *


class HousePagination(PageNumberPagination):

    page_size = 8
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 300


class HouseListView(generics.ListCreateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, DistanceToPointFilter, filters.SearchFilter, DjangoFilterBackend, InPolygonFilter)
    filter_class = HouseFilter

    pagination_class = HousePagination

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = HouseSerializer(data=request.data)
        # print(serializer)
        if serializer.is_valid(raise_exception=True):
            # print(serializer.validated_data)
            house = serializer.save()
            if house:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HouseView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HouseSerializer
    queryset = House.objects.all()


class HouseLocationListView(generics.ListCreateAPIView):
    queryset = HouseLocation.objects.all()
    serializer_class = LocationSerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter,)


class HouseInPolygonListView(generics.ListCreateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    ploygon_filter_field = 'location'
    filter_backends = (InPolygonFilter,)

    pagination_class = HousePagination

    def get(self, request, *args, **kwargs):

        return Response('Invalid request.', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BMHouseListView(generics.ListCreateAPIView):
    queryset = BMHouse.objects.all().order_by('-id')
    serializer_class = BMHouseSerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, DistanceToPointFilter, filters.SearchFilter, DjangoFilterBackend, InPolygonFilter,)
    search_fields = ('zipcode',)
    # filterset_fields = ('zipcode')
    filter_class = HouseFilter

    pagination_class = HousePagination

    def post(self, request, *args, **kwargs):
        print(request.data)

        serializer = BMHouseSerializer(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            # print(serializer.validated_data)
            house = serializer.save()
            if house:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BMHouseView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BMHouseSerializer
    lookup_field = 'uuid'
    queryset = BMHouse.objects.all()


class BMHouseInPolygonListView(generics.ListCreateAPIView):
    queryset = BMHouse.objects.all()
    serializer_class = BMHouseSerializer
    ploygon_filter_field = 'location'
    filter_backends = (InPolygonFilter,)

    pagination_class = HousePagination

    def get(self, request, *args, **kwargs):

        return Response('Invalid request.', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
