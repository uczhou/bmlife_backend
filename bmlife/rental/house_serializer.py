from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from rest_framework import serializers
from .models import *
from django.contrib.gis.geos import Point


class RentalDateField(serializers.Field):

    def to_representation(self, value):
        ret = {
            "starttime": value.starttime,
            "endtime": value.endtime
        }
        return ret

    def to_internal_value(self, data):
        ret = {
            "starttime": data["starttime"],
            "endtime": data["endtime"],
        }
        return ret


class ContactField(serializers.Field):

    def to_representation(self, value):
        ret = {
            "phonenumber": value.phonenumber,
            "email": value.email,
            "wechat": value.wechat
        }
        return ret

    def to_internal_value(self, data):
        ret = {
            "phonenumber": data["phonenumber"],
            "email": data["email"],
            "wechat": data["wechat"]
        }
        return ret


class DescriptionField(serializers.Field):
    def to_representation(self, value):
        ret = {
            "title": value.title,
            "description": value.description
        }
        return ret

    def to_internal_value(self, data):
        ret = {
            "title": data["title"],
            "description": data["description"],
        }
        return ret


class BasicInfoField(serializers.Field):
    def to_representation(self, value):
        ret = {
            "price": value.price,
            "housetype": value.housetype,
            "roomtype": value.roomtype,
            "bathroom": value.bathroom,
            "parkinglot": value.parkinglot,
            "washingmachine": value.washingmachine,
            "included": [{"included": val} for val in value.included.split('|')],
            "nearby": [{"nearby": val} for val in value.nearby.split('|')]
        }
        return ret

    def to_internal_value(self, data):
        included = [item['included'] for item in data['included']]
        nearby = [item['nearby'] for item in data['nearby']]

        ret = {
            "price": data['price'],
            "housetype":data['housetype'],
            "roomtype": data['roomtype'],
            "bathroom": data['bathroom'],
            "parkinglot":data['parkinglot'],
            "washingmachine": data['washingmachine'],
            "included": '|'.join(included),
            "nearby": '|'.join(nearby)
        }
        return ret


class RequirementField(serializers.Field):
    def to_representation(self, value):
        ret = {
            "leaseperiod": value.leaseperiod,
            "gender": value.gender,
            "cooking": value.cooking,
            "smoking": value.smoking,
            "otherrequirements": [{"otherrequirement": val} for val in value.otherrequirements.split('|')]
        }
        return ret

    def to_internal_value(self, data):
        otherrequirements = [item['otherrequirement'] for item in data['otherrequirements']]
        ret = {
            "leaseperiod": data['leaseperiod'],
            "gender":data['gender'],
            "cooking": data['cooking'],
            "smoking": data['smoking'],
            "otherrequirements": '|'.join(otherrequirements)
        }
        return ret


class ImagesField(serializers.Field):
    def to_representation(self, value):
        ret = [{"image": val} for val in value.images.split('|')]

        return ret

    def to_internal_value(self, data):
        images = [item['image'] for item in data]
        ret = {
            "images": '|'.join(images)
        }
        return ret


class BMHouseSerializer(GeoFeatureModelSerializer):

    uuid = serializers.CharField(required=True)
    category = serializers.CharField(required=False, default='Lease')
    fulladdress = serializers.CharField(required=False, default='No Data')
    address = serializers.CharField(required=False, default='')
    city = serializers.CharField(required=False, default='No Data')
    state = serializers.CharField(required=False, default='No Data')
    zipcode = serializers.CharField(required=False, default='No Data')
    longitude = serializers.CharField(required=False, default='41.8781')
    latitude = serializers.CharField(required=False, default='87.6298')

    location = GeometrySerializerMethodField(required=False)

    submittime = serializers.CharField(required=False, default='No Data')

    date = RentalDateField(source='*')

    description = DescriptionField(source='*')

    contact = ContactField(source='*')

    base = BasicInfoField(source='*')

    requirement = RequirementField(source='*')

    images = ImagesField(source='*')

    videos = serializers.CharField(required=False, default='No Data')

    def get_location(self, obj):
        return obj.location

    def create(self, validated_data):

        uuid = validated_data.get('uuid')
        category = validated_data.get('category')

        fulladdress = validated_data.get('fulladdress')
        address = validated_data.get('address')

        city = validated_data.get('city')
        state = validated_data.get('state')
        zipcode = validated_data.get('zipcode')
        submittime = validated_data.get('submittime')

        longitude = validated_data.get('longitude')
        latitude = validated_data.get('latitude')
        location = Point(float(longitude), float(latitude))

        starttime = validated_data.get('starttime')
        endtime = validated_data.get('endtime')

        title = validated_data.get('title')
        description = validated_data.get('description')

        phonenumber = validated_data.get('phonenumber')
        email = validated_data.get('email')
        wechat = validated_data.get('wechat')

        price = validated_data.get('price')
        housetype = validated_data.get('housetype')
        roomtype = validated_data.get('roomtype')
        bathroom = validated_data.get('bathroom')
        parkinglot = validated_data.get('parkinglot')
        washingmachine = validated_data.get('washingmachine')
        included = validated_data.get('included')
        nearby = validated_data.get('nearby')

        leaseperiod = validated_data.get('leaseperiod')
        gender = validated_data.get('gender')
        cooking = validated_data.get('cooking')
        smoking = validated_data.get('smoking')
        otherrequirements = validated_data.get('otherrequirements')

        images = validated_data.get('images')

        videos = validated_data.get('videos')

        house = BMHouse(uuid=uuid)

        house.category = category

        house.fulladdress = fulladdress
        house.address = address
        house.city = city
        house.state = state
        house.zipcode = zipcode
        house.longitude = longitude
        house.latitude = latitude
        house.location = location

        house.submittime = submittime

        house.starttime = starttime
        house.endtime = endtime

        house.title = title
        house.description = description

        house.phonenumber = phonenumber
        house.email = email
        house.wechat = wechat

        house.price = price
        house.housetype = housetype
        house.roomtype = roomtype

        house.bathroom = bathroom
        house.parkinglot = parkinglot
        house.washingmachine = washingmachine
        house.included = included
        house.nearby = nearby

        house.leaseperiod = leaseperiod
        house.gender = gender
        house.cooking = cooking
        house.smoking = smoking
        house.otherrequirements = otherrequirements

        house.images = images

        house.videos = videos

        # print(house)

        house.save()

        return house

    def update(self, instance, validated_data):

        uuid = validated_data.get('uuid')
        category = validated_data.get('category')

        fulladdress = validated_data.get('fulladdress')
        address = validated_data.get('address')

        city = validated_data.get('city')
        state = validated_data.get('state')
        zipcode = validated_data.get('zipcode')
        submittime = validated_data.get('submittime')

        longitude = validated_data.get('longitude')
        latitude = validated_data.get('latitude')
        location = Point(float(longitude), float(latitude))

        starttime = validated_data.get('starttime')
        endtime = validated_data.get('endtime')

        title = validated_data.get('title')
        description = validated_data.get('description')

        phonenumber = validated_data.get('phonenumber')
        email = validated_data.get('email')
        wechat = validated_data.get('wechat')

        price = validated_data.get('price')
        housetype = validated_data.get('housetype')
        roomtype = validated_data.get('roomtype')
        bathroom = validated_data.get('bathroom')
        parkinglot = validated_data.get('parkinglot')
        washingmachine = validated_data.get('washingmachine')
        included = validated_data.get('included')
        nearby = validated_data.get('nearby')

        leaseperiod = validated_data.get('leaseperiod')
        gender = validated_data.get('gender')
        cooking = validated_data.get('cooking')
        smoking = validated_data.get('smoking')
        otherrequirements = validated_data.get('otherrequirements')

        images = validated_data.get('images')

        videos = validated_data.get('videos')

        instance.uuid = uuid
        instance.category = category

        instance.fulladdress = fulladdress
        instance.address = address
        instance.city = city
        instance.state = state
        instance.zipcode = zipcode
        instance.longitude = longitude
        instance.latitude = latitude
        instance.location = location

        instance.submittime = submittime

        instance.starttime = starttime
        instance.endtime = endtime

        instance.title = title
        instance.description = description

        instance.phonenumber = phonenumber
        instance.email = email
        instance.wechat = wechat

        instance.price = price
        instance.housetype = housetype
        instance.roomtype = roomtype

        instance.bathroom = bathroom
        instance.parkinglot = parkinglot
        instance.washingmachine = washingmachine
        instance.included = included
        instance.nearby = nearby

        instance.leaseperiod = leaseperiod
        instance.gender = gender
        instance.cooking = cooking
        instance.smoking = smoking
        instance.otherrequirements = otherrequirements

        instance.images = images

        instance.videos = videos

        instance.save()

        return instance

    class Meta:
        model = BMHouse
        geo_field = 'location'
        fields = ('id', 'uuid', 'category', 'fulladdress', 'address', 'city', 'state', 'zipcode', 'submittime',
                  'longitude', 'latitude', 'date', 'description', 'contact', 'base', 'requirement', 'images', 'videos')
        # fields = ('id', 'uuid', 'category', 'fulladdress', 'address', 'city', 'state', 'zipcode', 'submittime',
        #           'longitude', 'latitude', 'title', 'description', 'starttime', 'endtime',
        #           'phonenumber', 'email', 'wechat', 'price', 'housetype', 'roomtype', 'bathroom',
        #           'parkinglot', 'washingmachine', 'included', 'nearby',
        #           'leaseperiod', 'gender', 'cooking', 'smoking', 'otherrequirements',
        #           'images', 'videos')