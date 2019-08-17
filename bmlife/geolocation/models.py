# from django.db import models
from django.contrib.gis.db import models


# Create your models here.
class State(models.Model):

    gid = models.AutoField(primary_key=True)
    region = models.CharField(max_length=2)
    division = models.CharField(max_length=2)
    statefp = models.CharField(max_length=2)
    statens = models.CharField(max_length=8)
    geoid = models.CharField(max_length=2)
    stusps = models.CharField(max_length=2)
    name = models.CharField(max_length=100)
    lsad = models.CharField(max_length=2)
    mtfcc = models.CharField(max_length=5)
    funcstat = models.CharField(max_length=1)
    aland = models.FloatField()
    awater = models.FloatField()
    intptlat = models.CharField(max_length=11)
    intptlon = models.CharField(max_length=12)
    geom = models.MultiPolygonField(dim=2)

    class Meta:
        managed = False
        db_table = 'state'


class UrbanArea(models.Model):

    gid = models.AutoField(primary_key=True)
    uace10 = models.CharField(max_length=5)
    geoid10 = models.CharField(max_length=5)
    name10 = models.CharField(max_length=100)
    namelsad10 = models.CharField(max_length=100)
    lsad10 = models.CharField(max_length=2)
    mtfcc10 = models.CharField(max_length=5)
    uatyp10 = models.CharField(max_length=1)
    funcstat10 = models.CharField(max_length=1)
    aland10 = models.FloatField()
    awater10 = models.FloatField()
    intptlat10 = models.CharField(max_length=11)
    intptlon10 = models.CharField(max_length=12)
    geom = models.MultiPolygonField(dim=2)

    class Meta:
        managed = False
        db_table = 'city'


class County(models.Model):

    gid = models.AutoField(primary_key=True)
    statefp = models.CharField(max_length=2)
    countyfp = models.CharField(max_length=3)
    countyns = models.CharField(max_length=8)
    geoid = models.CharField(max_length=2)
    name = models.CharField(max_length=100)
    namelsad = models.CharField(max_length=100)
    lsad = models.CharField(max_length=2)
    classfp = models.CharField(max_length=2)
    mtfcc = models.CharField(max_length=5)
    csafp = models.CharField(max_length=3)
    cbsafp = models.CharField(max_length=5)
    metdivfp = models.CharField(max_length=5)
    funcstat = models.CharField(max_length=1)
    aland = models.FloatField()
    awater = models.FloatField()
    intptlat = models.CharField(max_length=11)
    intptlon = models.CharField(max_length=12)
    geom = models.MultiPolygonField(dim=2)

    class Meta:
        managed = False
        db_table = 'county'


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
    geom = models.MultiPolygonField(dim=2)

    class Meta:
        managed = False
        db_table = 'zipcode'
