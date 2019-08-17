import psycopg2
from scrapy.pipelines.images import ImagesPipeline
import hashlib
from PIL import Image
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
from scrapy.utils.python import to_bytes
from scrapy.http import Request, FormRequest
from urllib.parse import urlparse
from .item import *
from .utils.geocode import get_coordinate
import json
import time
from scrapy.exceptions import DropItem

default_headers = {}


class BmlifeBotPipeline(object):

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        print('----------------------------------------------')
        url = 'http://127.0.0.1:8000/api/v1/rental/house/'
        payload = {
            "uuid": item['uuid'],
            "category": item['category'],
            "fulladdress": item['full_address'],
            "address": item['address'],
            "city": item['city'],
            "state": item['state'],
            "zipcode": item['zipcode'],
            "submittime": item['submittime'],
            "longitude": item['longitude'],
            "latitude": item['latitude'],
            "date": {
                "starttime": item['starttime'],
                "endtime": item['endtime']
            },
            "description": {
                "title": item['title'],
                "description": item['description']
            },
            "contact": {
                "phonenumber": item['phonenumber'],
                "email": item['email'],
                "wechat": item['wechat']
            },
            "base": {
                "price": item['price'],
                "housetype": item['house_type'],
                "roomtype": item['room_type'],
                "bathroom": item['bathroom'],
                "parkinglot": item['parkinglot'],
                "washingmachine": item['washingmachine'],
                "nearby": [{"nearby": value} for value in item['nearby']],
                "included": [{"included": value} for value in item['included']]
            },
            "requirement": {
                "leaseperiod": item['leaseperiod'],
                "gender": item['gender'],
                "cooking": item['cooking'],
                "smoking": item['smoking'],
                "otherrequirements": [{"otherrequirement": value} for value in item['otherrequirements']]
            },
            "images": [{"image": value} for value in item['images']],
            "videos": item['videos']
        }

        self.crawler.engine.crawl(

            Request(url, method="POST", body=json.dumps(payload), headers={'Content-Type': 'application/json'}),
            spider,
        )

        time.sleep(2)

        return item

    def parse(self, response):
        print(response.body)


class BmlifeImageDownloaderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        print('**************************In Image Download Pipeline***********************************')
        if isinstance(item, HouseItem):
            for image_url in item['image_urls']:
                # print(image_url)
                try:
                    print('Downloading Image: {}'.format(image_url))
                    default_headers['Referer'] = item['referer']
                    default_headers['Host'] = urlparse(image_url).netloc
                    yield Request(image_url, headers=default_headers,
                                  meta={"dont_retry": False, "dont_redirect": True, "max_retry_times": 3})
                except Exception as e:
                    print(e)
                    continue
        else:
            return item

    def item_completed(self, results, item, info):
        print('************************************************')
        if isinstance(item, HouseItem):
            image_paths = [{hashlib.sha1(x['url'].encode('utf-8')).hexdigest(): x['path']} for ok, x in results if ok]
            item['dest_urls'] = image_paths
            images = ['https://blissmotors-web-upload.s3.amazonaws.com/bmlife/{}'.format(x['path']) for ok, x in results if ok]
            item['images'] = images
            if len(images) > 0:
                lat, lon = get_coordinate(item['full_address'])

                item['latitude'] = str(lat)
                item['longitude'] = str(lon)
                return item
            else:
                raise DropItem()
        else:
            raise DropItem()

    def file_path(self, request, response=None, info=None):
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)

        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation

        if '.png' in request.url:
            return 'full/%s.png' % (image_guid)
        else:
            return 'full/%s.jpg' % (image_guid)

    def convert_image(self, image, size=None):
        flag = 'JPEG'
        if image.format == 'PNG' and image.mode == 'RGBA':
            flag = 'PNG'
            # background = Image.new('RGBA', image.size, (255, 255, 255))
            # background.paste(image, image)
            # image = background.convert('RGB')
        elif image.mode == 'P':  # Here follows the changes from the original Scrapy 1.3.2 code
            image = image.convert("RGBA")
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)

        buf = BytesIO()
        if flag == 'PNG':
            image.save(buf, 'PNG')
        else:
            image.save(buf, 'JPEG')
        return image, buf
