from rest_framework.filters import BaseFilterBackend
from django.db.models import Q
from rest_framework.exceptions import ParseError
from django.contrib.gis.geos import Polygon, Point
import django_filters
from .models import *


class InPolygonFilter(BaseFilterBackend):
    polygon_param = 'in_polygon'

    def get_filter_bbox(self, request):
        bbox_string = request.data.get(self.polygon_param, None)
        if not bbox_string:
            return None
        try:
            data = [float(n) for n in bbox_string.split(',')]
        except ValueError:
            raise ParseError('Invalid bbox string supplied for parameter {0}'.format(self.polygon_param))
        points = []
        for i in range(0, len(data) - 1, 2):
            points.append((data[i], data[i+1]))
        x = Polygon(tuple(points))
        return x

    def filter_queryset(self, request, queryset, view):

        filter_field = getattr(view, 'ploygon_filter_field', None)
        include_overlapping = getattr(view, 'ploygon_filter_include_overlapping', False)
        if include_overlapping:
            geoDjango_filter = 'bboverlaps'
        else:
            geoDjango_filter = 'contained'

        if not filter_field:
            return queryset

        bbox = self.get_filter_bbox(request)
        if not bbox:
            return queryset
        return queryset.filter(Q(**{'%s__%s' % (filter_field, geoDjango_filter): bbox})).order_by('-id')


class HouseFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr='iexact')
    state = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = BMHouse
        fields = ['city', 'state']
