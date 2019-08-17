from django.db import models
from django.db.models.base import ModelBase
from django.contrib.gis.db import models as gis_models

def get_model(table_name):

    class CrimeSpotMetaclass(ModelBase):
        def __new__(cls, name, bases, attrs):
            name = table_name
            return ModelBase.__new__(cls, name, bases, attrs)

    class CrimeSpot(models.Model, metaclass=CrimeSpotMetaclass):

        gid = models.AutoField(primary_key=True)

        address_1 = models.TextField(null=True)
        case_number = models.TextField(null=True)
        city = models.CharField(max_length=50)

        created_at = models.TextField(null=True)
        day_of_week = models.CharField(max_length=50)
        hour_of_day = models.CharField(max_length=50)
        incident_datetime = models.TextField(null=True)
        incident_id = models.CharField(max_length=75)
        incident_type_primary = models.TextField(null=True)
        latitude = models.CharField(max_length=50)
        longitude = models.CharField(max_length=50)
        location = gis_models.PointField(dim=2)
        parent_incident_type = models.TextField(null=True)
        state = models.CharField(max_length=10)
        updated_at = models.TextField(null=True)
        zip = models.CharField(max_length=10)

        class Meta:
            managed = False
            db_table = table_name
    return CrimeSpot


class ZipCode(models.Model):
    gid = models.AutoField(primary_key=True)
    crimecount = models.IntegerField()
    zcta5ce10 = models.CharField(max_length=5)
    geoid10 = models.CharField(max_length=5)
    classfp10 = models.CharField(max_length=2)
    mtfcc10 = models.CharField(max_length=5)
    funcstat10 = models.CharField(max_length=1)
    aland10 = models.FloatField()
    awater10 = models.FloatField()
    intptlat10 = models.CharField(max_length=11)
    intptlon10 = models.CharField(max_length=12)
    geom = gis_models.PolygonField(dim=2)

    class Meta:
        managed = False
        db_table = 'zipcode'