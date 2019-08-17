from django.contrib.gis.db import models


class HouseLocation(models.Model):

    id = models.AutoField(primary_key=True)
    longitude = models.TextField()
    latitude = models.TextField()
    location = models.PointField(dim=2)


class HouseRentalDate(models.Model):
    id = models.AutoField(primary_key=True)
    starttime = models.TextField()
    endtime = models.TextField()


class HouseDescription(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.TextField()
    description = models.TextField()


class HouseContact(models.Model):

    id = models.AutoField(primary_key=True)
    phonenumber = models.TextField()
    email = models.TextField()
    wechat = models.TextField()


class HouseBasicInfo(models.Model):

    id = models.AutoField(primary_key=True)
    price = models.TextField()
    housetype = models.TextField()
    roomtype = models.TextField()
    bathroom = models.TextField()
    parkinglot = models.TextField()
    washingmachine = models.TextField()


class HouseRequirement(models.Model):
    id = models.AutoField(primary_key=True)
    leaseperiod = models.TextField()
    gender = models.TextField()
    cooking = models.TextField()
    smoking = models.TextField()


class HouseIncluded(models.Model):

    id = models.AutoField(primary_key=True)
    base = models.ForeignKey(HouseBasicInfo,
                             on_delete=models.CASCADE,
                             related_name="included",
                             related_query_name='included',
                             null=True, blank=True)
    # uuid = models.TextField()
    included = models.TextField()


class HouseNearby(models.Model):
    id = models.AutoField(primary_key=True)
    base = models.ForeignKey(HouseBasicInfo,
                             on_delete=models.CASCADE,
                             related_name="nearby",
                             related_query_name='nearby',
                             null=True, blank=True)
    nearby = models.TextField()


class HouseOtherRequirement(models.Model):
    id = models.AutoField(primary_key=True)
    requirement = models.ForeignKey(HouseRequirement,
                                    on_delete=models.CASCADE,
                                    related_name="otherrequirements",
                                    related_query_name='otherrequirements',
                                    null=True, blank=True)
    otherrequirement = models.TextField()


class House(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.TextField()
    category = models.CharField(max_length=20, default='Lease')

    fulladdress = models.TextField()
    address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zipcode = models.TextField()

    longitude = models.TextField()
    latitude = models.TextField()
    location = models.PointField(spatial_index = True,
                                srid = 4326,
                                 geography=True)

    submittime = models.TextField()

    videos = models.TextField()

    valid = models.CharField(max_length=5, default='1')

    date = models.OneToOneField(
        HouseRentalDate,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    description = models.OneToOneField(
        HouseDescription,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    contact = models.OneToOneField(
        HouseContact,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    base = models.OneToOneField(
        HouseBasicInfo,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    requirement = models.OneToOneField(
        HouseRequirement,
        on_delete=models.CASCADE,
        null=True, blank=True
    )


class HouseImage(models.Model):

    id = models.AutoField(primary_key=True)
    house = models.ForeignKey(House,
                              on_delete=models.CASCADE,
                              related_name="images",
                              related_query_name='images',
                              null=True, blank=True)
    image = models.TextField()


class BMHouse(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.TextField()
    category = models.CharField(max_length=20, default='Leasing')

    fulladdress = models.TextField()
    address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zipcode = models.TextField()

    longitude = models.TextField()
    latitude = models.TextField()
    location = models.PointField(spatial_index = True,
                                 srid = 4326,
                                 geography=True)

    submittime = models.TextField()

    # Date
    starttime = models.TextField()
    endtime = models.TextField()

    # Description
    title = models.TextField()
    description = models.TextField()

    # Contact
    phonenumber = models.TextField()
    email = models.TextField()
    wechat = models.TextField()

    # Basic Info
    price = models.TextField()
    housetype = models.TextField()
    roomtype = models.TextField()
    bathroom = models.TextField()
    parkinglot = models.TextField()
    washingmachine = models.TextField()
    included = models.TextField()
    nearby = models.TextField()

    # Requirements
    leaseperiod = models.TextField()
    gender = models.TextField()
    cooking = models.TextField()
    smoking = models.TextField()
    otherrequirements = models.TextField()

    images = models.TextField()

    videos = models.TextField()
    valid = models.CharField(max_length=5, default='1')

