# Generated by Django 2.1.8 on 2019-06-02 03:25

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geolocation', '0005_county'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZipCode',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('zcta5ce10', models.CharField(max_length=5)),
                ('geoid10', models.CharField(max_length=5)),
                ('classfp10', models.CharField(max_length=2)),
                ('mtfcc10', models.CharField(max_length=5)),
                ('funcstat10', models.CharField(max_length=1)),
                ('aland10', models.FloatField()),
                ('awater10', models.FloatField()),
                ('intptlat10', models.CharField(max_length=11)),
                ('intptlon10', models.CharField(max_length=12)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'db_table': 'zipcode',
                'managed': False,
            },
        ),
    ]
