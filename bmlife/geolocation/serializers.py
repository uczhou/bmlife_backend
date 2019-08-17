from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import *


class StateSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = State
        geo_field = 'geom'
        # auto_bbox = True
        fields = ('gid', 'stusps', 'name')


class UrbanAreaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = UrbanArea
        geo_field = 'geom'
        # auto_bbox = True
        fields = ('gid', 'name10')


class CountySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = County
        geo_field = 'geom'
        # auto_bbox = True
        fields = ('gid', 'name', 'intptlon', 'intptlat')


class ZipCodeSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ZipCode
        geo_field = 'geom'
        # auto_bbox = True
        fields = ('gid', 'zcta5ce10', 'crimecount')
