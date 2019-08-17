from scrapy.item import Item, Field


class BmlifeItem(Item):
    # define the fields for your item here like:
    name = Field()
    id = Field()
    url = Field()
    link = Field()
    file_urls = Field()
    uuid = Field()


class HouseItem(Item):

    uuid = Field()

    category = Field()
    full_address = Field()
    address = Field()
    city = Field()
    state = Field()
    zipcode = Field()
    submittime = Field()

    longitude = Field()
    latitude = Field()

    starttime = Field()
    endtime = Field()

    phonenumber = Field()
    email = Field()
    wechat = Field()

    title = Field()
    description = Field()

    price = Field()
    house_type = Field()
    room_type = Field()
    bathroom = Field()
    parkinglot = Field()
    washingmachine = Field()

    nearby = Field()   # List
    included = Field()  # List

    leaseperiod = Field()
    gender = Field()
    cooking = Field()
    smoking = Field()
    otherrequirements = Field()  # List

    videos = Field()

    referer = Field()

    url_mapping = Field()

    image_urls = Field()
    images = Field()  # List
    dest_urls = Field()


