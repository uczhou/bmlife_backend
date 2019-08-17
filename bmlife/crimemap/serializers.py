from rest_framework_gis.serializers import GeoFeatureModelSerializer


class CrimeSerializer(GeoFeatureModelSerializer):

    def get_location(self, obj):
        return obj.location

    class Meta:
        model = None
        geo_field = 'location'
        fields = ('gid', 'address_1', 'city', 'state', 'zip', 'incident_datetime',
                  'longitude', 'latitude', 'parent_incident_type')
