from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from rest_framework import serializers
from .models import *
from django.contrib.gis.geos import Point


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = HouseImage
        fields = ('id', 'image')


class IncludedSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseIncluded
        fields = ('id', 'included')


class NearbySerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseNearby
        fields = ('id', 'nearby')


class OtherRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseOtherRequirement
        fields = ('id', 'otherrequirement')


class LocationSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = HouseLocation
        geo_field = 'location'
        fields = ('id', 'longitude', 'latitude')


class RentalDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HouseRentalDate
        fields = ('id', 'starttime', 'endtime')


class DescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = HouseDescription
        fields = ('id', 'title', 'description')


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = HouseContact
        fields = ('id', 'phonenumber', 'email', 'wechat')


class BasicInfoSerializer(serializers.ModelSerializer):
    nearby = NearbySerializer(many=True, required=False)
    included = IncludedSerializer(many=True, required=False)

    class Meta:
        model = HouseBasicInfo
        fields = ('id', 'price', 'housetype', 'roomtype', 'bathroom', 'parkinglot', 'washingmachine', 'nearby', 'included')


class RequirementSerializer(serializers.ModelSerializer):

    otherrequirements = OtherRequirementSerializer(many=True, required=False)

    class Meta:
        model = HouseRequirement
        fields = ('id', 'leaseperiod', 'gender', 'cooking', 'smoking', 'otherrequirements')


class HouseSerializer(GeoFeatureModelSerializer):
    images = ImageSerializer(many=True, required=False)
    date = RentalDateSerializer(required=False)
    description = DescriptionSerializer(required=False)
    contact = ContactSerializer(required=False)
    base = BasicInfoSerializer(required=False)
    requirement = RequirementSerializer(required=False)

    uuid = serializers.CharField(required=True)
    category = serializers.CharField(required=False, default='Lease')
    fulladdress = serializers.CharField(required=False, default='')
    address = serializers.CharField(required=False, default='')
    city = serializers.CharField(required=False, default='')
    state = serializers.CharField(required=False, default='')
    zipcode = serializers.CharField(required=False, default='')
    longitude = serializers.CharField(required=False, default='41.8781')
    latitude = serializers.CharField(required=False, default='87.6298')

    location = GeometrySerializerMethodField(required=False)

    submittime = serializers.CharField(required=False, default='')

    videos = serializers.CharField(required=False, default='')

    def get_location(self, obj):
        return obj.location

    def create(self, validated_data):

        uuid = validated_data.get('uuid')
        category = validated_data.get('category')
        print(validated_data)
        fulladdress = validated_data.get('fulladdress')
        address = validated_data.get('address')

        city = validated_data.get('city')
        state = validated_data.get('state')
        zipcode = validated_data.get('zipcode')
        submittime = validated_data.get('submittime')

        longitude = validated_data.get('longitude')
        latitude = validated_data.get('latitude')
        location = Point(float(longitude), float(latitude))

        # Date
        rental_date = validated_data.get('date')
        # print(rental_date)

        # Description
        house_description = validated_data.get('description')

        # Contact
        contact_info = validated_data.get('contact')

        # Base
        basic_info = validated_data.get('base')

        # Requirement
        rental_requirement = validated_data.get('requirement')

        images_data = validated_data.get('images')

        videos = validated_data.get('videos')

        if rental_date:
            # print(rental_date)
            date = HouseRentalDate()
            date.starttime = rental_date.get('starttime')
            date.endtime = rental_date.get('endtime')
            date.save()

        if house_description:
            # print(house_description)
            description = HouseDescription()
            description.title = house_description.get('title')
            description.description = house_description.get('description')
            description.save()

        if contact_info:
            # print(contact_info)
            contact = HouseContact()
            contact.phonenumber = contact_info.get('phonenumber')
            contact.email = contact_info.get('email')
            contact.wechat = contact_info.get('wechat')
            contact.save()

        if basic_info:
            # print(basic_info)
            base = HouseBasicInfo()
            base.price = basic_info.get('price')
            base.housetype = basic_info.get('housetype')
            base.roomtype = basic_info.get('roomtype')
            base.bathroom = basic_info.get('bathroom')
            base.parkinglot = basic_info.get('parkinglot')
            base.washingmachine = basic_info.get('washingmachine')

            base.save()

            includeds_data = basic_info.get('included')
            nearbys_data = basic_info.get('nearby')

            for included_data in includeds_data:
                included_instance = HouseIncluded(base=base)
                included_instance.included = included_data.get('included')
                included_instance.save()

            for nearby_data in nearbys_data:
                nearby_instance = HouseNearby(base=base)
                nearby_instance.nearby = nearby_data.get('nearby')
                nearby_instance.save()

        if rental_requirement:
            requirement = HouseRequirement()
            requirement.leaseperiod = rental_requirement.get('leaseperiod')
            requirement.gender = rental_requirement.get('gender')
            requirement.cooking = rental_requirement.get('cooking')
            requirement.smoking = rental_requirement.get('smoking')
            requirement.save()

            otherrequirements_data = rental_requirement.get('otherrequirements')

            for otherrequirement_data in otherrequirements_data:
                otherrequirement_instance = HouseOtherRequirement(requirement=requirement)
                otherrequirement_instance.otherrequirement = otherrequirement_data.get('otherrequirement')
                otherrequirement_instance.save()

        house = House(uuid=uuid)

        if date:
            house.date = date
        if description:
            house.description = description
        if contact:
            house.contact = contact
        if base:
            house.base = base
        if requirement:
            house.requirement = requirement

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
        house.videos = videos

        # print(house)

        house.save()

        # Image
        for image_data in images_data:
            print(image_data.get('image'))
            image_instance = HouseImage(house=house)
            image_instance.image = image_data.get('image')
            image_instance.save()

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

        # Date
        rental_date = validated_data.get('date')

        # Description
        house_description = validated_data.get('description')

        # Contact
        contact_info = validated_data.get('contact')

        # Base
        basic_info = validated_data.get('base')

        # Requirement
        rental_requirement = validated_data.get('requirement')

        images_data = validated_data.get('images')

        videos = validated_data.get('videos')

        instance.uuid = uuid
        instance.category = category
        instance.fulladdress = fulladdress
        instance.address = address
        instance.city = city
        instance.state = state
        instance.zipcode = zipcode

        instance.submittime = submittime
        instance.videos = videos

        instance.longitude = longitude
        instance.latitude = latitude
        instance.location = location

        instance.save()

        if rental_date:
            date = HouseRentalDate(house=instance)
            date.starttime = rental_date.get('starttime')
            date.endtime = rental_date.get('endtime')
            date.save()

        if house_description:
            description = HouseDescription(house=instance)
            description.title = house_description.get('title')
            description.description = house_description.get('description')
            description.save()

        if contact_info:
            contact = HouseContact(house=instance)
            contact.phonenumber = contact_info.get('phonenumber')
            contact.email = contact_info.get('email')
            contact.wechat = contact_info.get('wechat')
            contact.save()

        if basic_info:
            base = HouseBasicInfo(house=instance)
            base.price = basic_info.get('price')
            base.housetype = basic_info.get('housetype')
            base.roomtype = basic_info.get('roomtype')
            base.bathroom = basic_info.get('bathroom')
            base.parkinglot = basic_info.get('parkinglot')
            base.washingmachine = basic_info.get('washingmachine')

            base.save()

            includeds_data = basic_info.get('included')
            nearbys_data = basic_info.get('nearby')

            for included_data in includeds_data:
                included_instance = HouseIncluded(base=base)
                included_instance.name = included_data
                included_instance.save()

            for nearby_data in nearbys_data:
                nearby_instance = HouseNearby(base=base)
                nearby_instance.name = nearby_data
                nearby_instance.save()

        if rental_requirement:
            requirement = HouseRequirement(house=instance)
            requirement.leaseperiod = rental_requirement.get('leaseperiod')
            requirement.gender = rental_requirement.get('gender')
            requirement.cooking = rental_requirement.get('cooking')
            requirement.smoking = rental_requirement.get('smoking')
            requirement.save()

            otherrequirements_data = rental_requirement.get('otherrequirements')

            for otherrequirement_data in otherrequirements_data:
                otherrequirement_instance = HouseOtherRequirement(requirement=requirement)
                otherrequirement_instance.name = otherrequirement_data
                otherrequirement_instance.save()
        # Image
        for image_data in images_data:
            image_instance = HouseImage(house=instance)
            image_instance.image = image_data
            image_instance.save()

        return instance

    class Meta:
        model = House
        geo_field = 'location'
        fields = ('id', 'uuid', 'category', 'fulladdress', 'address', 'city', 'state', 'zipcode', 'submittime',
                  'longitude', 'latitude', 'date', 'description', 'contact', 'base', 'requirement', 'images', 'videos')