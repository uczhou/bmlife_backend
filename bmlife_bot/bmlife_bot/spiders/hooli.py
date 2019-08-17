import scrapy
from scrapy.selector import Selector
from urllib.parse import urljoin
from ..item import *
import re
import datetime
import uuid


class HooliSpider(scrapy.Spider):
    name = 'hooli'


    def __init__(self, *args, **kwargs):

        super(HooliSpider, self).__init__(*args, **kwargs)

    def start_requests(self):

        start_urls = [
            {'url': 'http://www.hoolihome.com/cn/Philadelphia/building-list/', 'state': 'PA', 'city': 'Philadelphia', 'page': 2},
            {'url': 'http://www.hoolihome.com/cn/Dallas/building-list/', 'state': 'TX', 'city': 'Dallas',
             'page': 1},
            {'url': 'http://www.hoolihome.com/cn/Boston/building-list/', 'state': 'MA', 'city': 'Boston',
             'page': 50},
            {'url': 'http://www.hoolihome.com/cn/San-Diego/building-list/', 'state': 'CA', 'city': 'San Diego',
             'page': 2},
            {'url': 'http://www.hoolihome.com/cn/New-York/building-list/', 'state': 'NY', 'city': 'New York',
             'page': 22},
            {'url': 'http://www.hoolihome.com/cn/Chicago/building-list/', 'state': 'IL', 'city': 'Chicago',
             'page': 3},
            {'url': 'http://www.hoolihome.com/cn/Seattle/building-list/', 'state': 'WA', 'city': 'Seattle',
             'page': 2},
            {'url': 'http://www.hoolihome.com/cn/Los-Angeles/building-list/', 'state': 'CA', 'city': 'Los Angeles',
             'page': 6},
            {'url': 'http://www.hoolihome.com/cn/Irvine/building-list/', 'state': 'CA', 'city': 'Irvine',
             'page': 2},
            {'url': 'http://www.hoolihome.com/cn/Minneapolis/building-list/', 'state': 'MN', 'city': 'Minneapolis',
             'page': 1},
            {'url': 'http://www.hoolihome.com/cn/Urbana-Champaign/building-list/', 'state': 'IL', 'city': 'Urbana-Champaign',
             'page': 9},
        ]

        for item in start_urls:
            for i in range(1, item.get('page') + 1):

                yield scrapy.Request('{}?page={}'.format(item['url'], i), meta={'state': item['state'], 'city': item['city']}, callback=self.parse)

    def parse(self, response):
        print(response.url)

        hxs = Selector(response)

        ul = hxs.xpath('//ul[@class="list-content"]/li')

        for li in ul:
            link = li.xpath('.//div[@class="house-item"]/div/a/@href').extract_first()
            print(link)

            url_data = urljoin(response.url, link)

            title = li.xpath('.//div[@class="house-info"]/div/h3/a/span/text()').get()
            print(title)

            yield scrapy.Request(url_data, meta=response.meta, callback=self.parse_detail)

    def parse_detail(self, response):

        print(response.url)

        hxs = Selector(response)

        meta_data = response.meta

        house = HouseItem()

        house['uuid'] = str(uuid.uuid4())

        # Images
        images = hxs.xpath('//div[@class="imgs-list"]/ul/li')

        image_urls = []
        for image in images:
            src = image.xpath('.//img/@src').extract_first()
            if src:
                # print(src.split('?')[0])
                image_urls.append(src.split('?')[0])

        house['image_urls'] = image_urls

        # Title
        house_title = hxs.xpath('//div[@class="house-title"]/h2/text()').get()
        house['title'] = house_title
        # print(house_title)

        # Address
        house_address = hxs.xpath('//div[@class="house-title"]/h4/span[@class="house-address-text can-copy"]/text()').get()

        house['full_address'] = house_address

        house['address'] = house_address.split(',')[0]
        # print(house_address)

        house['city'] = meta_data['city']
        house['state'] = meta_data['state']

        postal_code = re.search(r'(\d{5})([- ])?(\d{4})?', house_address)
        # print(postal_code)
        if postal_code is not None:
            house['zipcode'] = postal_code.group(0)

        house['submittime'] = datetime.date.today().strftime("%Y-%m-%d")

        # price = hxs.xpath('//p[@class="building-money"]/span')[1].xpath('.//text()').get()
        price = hxs.xpath('//p[@class="building-money"]/span[@class="building-price"]/text()').get()
        # print(price)

        # house['price'] = price

        introductions = hxs.xpath('//div[@id="introduction"]/div')

        intros = []
        for introduction in introductions:
            pp = introduction.xpath('.//p')
            for p in pp:
                text = p.xpath('.//text()').get()
                if text:
                    # print(text)
                    intros.append(text.strip().strip('\n'))
        if len(intros) > 0:
            house['description'] = '\n'.join(intros)

        else:
            house['description'] = 'empty'

        tags = hxs.xpath('//ul[@class="tags-list"]/li')

        nearby = []
        for tag in tags:
            t = tag.xpath('.//span/text()').get()
            nearby.append(t.strip().strip('\n'))
        if len(nearby) == 0:
            nearby.append('empty')
        house['nearby'] = nearby

        rooms = hxs.xpath('//div[@class="room-list"]/div[@class="room-content"]')
        for room in rooms:
            room_price = room.xpath('.//div[@class="room-checkin"]/p[@class="room-checkin-price"]/span[@class="price"]/text()').get()

            # print(room_price)

            house['price'] = room_price

            room_facilities = room.xpath('.//div[@class="room-facilities"]/span')
            if len(room_facilities) > 0:
                house['room_type'] = room_facilities[0].xpath('.//span')[0].xpath('.//text()').get()
                house['bathroom'] = room_facilities[-1].xpath('.//span')[0].xpath('.//text()').get()

            room_infos = room.xpath('.//div[@class="room-checkin-time"]/span')
            if len(room_infos) == 3:
                house['leaseperiod'] = room_infos[0].xpath('.//text()').get()
                starttime = room_infos[2].xpath('.//text()').get()
                if '随时入住' in starttime:
                    house['starttime'] = datetime.date.today().strftime("%Y-%m-%d")
                else:
                    house['starttime'] = starttime.strip().strip('\n')
                    if house['starttime'] is None or house['starttime'] == '':
                        house['starttime'] = datetime.date.today().strftime("%Y-%m-%d")

        facilities = hxs.xpath('//div[@id="facilities"]//ul[@class="each-wrap"]/li')

        included = []
        for facility in facilities:
            # print(facility.xpath('.//p[@class="item-name singleline"]/text()').get())
            include = facility.xpath('.//p[@class="item-name singleline"]/text()').get()
            included.append(include.strip().strip('\n'))
        if len(included) == 0:
            included.append('empty')
        house['included'] = included

        house['gender'] = 'Both'
        house['cooking'] = 'Normal Cooking'
        house['smoking'] = 'No Smoking'
        house['otherrequirements'] = ['Keep Clean']

        house['referer'] = response.url
        house['videos'] = 'empty'
        house['washingmachine'] = 'NA'
        house['parkinglot'] = 'NA'

        house['phonenumber'] = '4008986659'
        house['email'] = 'bmlifeservice@gmail.com'
        house['wechat'] = 'empty'

        house['category'] = 'Real Estate'
        house['endtime'] = 'empty'

        house['house_type'] = 'Apartment'

        yield house

