from .serializers import *
from .models import *
from .filter import *
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.filters import OrderingFilter


class CrimePagination(PageNumberPagination):

    page_size = 8
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 300


class CrimeListView(generics.ListCreateAPIView):
    ploygon_filter_field = 'location'
    filter_backends = (InPolygonFilter, OrderingFilter,)
    ordering_fields = ('incident_datetime',)

    pagination_class = CrimePagination

    def get_queryset(self):
        print(self.kwargs)
        print(self.request)
        state = self.kwargs.get('state', None)
        print(state)
        if state is None:
            return []
        table_name = 'crimemap_{}'.format(state)
        model = get_model(table_name)

        query_set = model.objects.all()
        print(query_set[0].location.srid)
        self.kwargs['model'] = model
        return query_set

    def get_serializer_class(self):
        print(self.kwargs)
        CrimeSerializer.Meta.model = self.kwargs.get('model')
        return CrimeSerializer

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
