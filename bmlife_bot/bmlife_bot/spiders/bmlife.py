# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from ..item.items import BmlifeItem
from urllib.parse import urljoin
import json
import hashlib


class BmlifeSpider(scrapy.Spider):
    name = "bmlife"
    allowed_domains = ["socrata.com"]
    visited = []
    start_urls = (
        'https://moto.data.socrata.com/browse?limitTo=datasets&page=1',
    )
    custom_settings = {'FEED_URI': "crimemap_%(time)s.json",
                       'FEED_FORMAT': 'json'}

    @staticmethod
    def _parse_json(response):
        key = response.url.split('/')[-1].split('.')[0]
        yield {
            key: json.loads(response.text)
        }

    @staticmethod
    def _parse_web(response):
        print('Parse Web')
        hxs = Selector(response)
        data = hxs.xpath("//div[@class='browse2-results']/div")
        print(len(data))
        for d in data:
            # print(d.extract())
            try:
                view_id = d.xpath("./@data-view-id").extract_first()
                view_name = d.xpath(".//div[@class='browse2-result-title']//a/text()").extract_first()
                link = d.xpath(".//div[@class='browse2-result-title']//a/@href").extract_first()
                url = 'https://moto.data.socrata.com/resource/{}.json'.format(view_id)
                file_url = 'https://moto.data.socrata.com/api/views/{}/rows.csv'.format(view_id)
                uuid_value = hashlib.sha1(file_url.encode('utf-8')).hexdigest()
                bmlife_item = BmlifeItem()
                bmlife_item['name'] = view_name
                bmlife_item['id'] = view_id
                bmlife_item['link'] = link
                bmlife_item['url'] = url
                bmlife_item['file_urls'] = [file_url]
                bmlife_item['uuid'] = uuid_value

                scrapy_info = {
                    'name': view_name,
                    'id': view_id,
                    'link': link,
                    'url': url
                }

                yield bmlife_item
                # yield scrapy_info

                # yield scrapy.Request(url)
            except Exception as e:
                print(e)
                continue

        links = hxs.xpath("//div[@class='pagination']/a")
        for link_data in links:
            link = link_data.xpath('.//@href').extract_first()
            url_data = urljoin(response.url, link)
            if url_data not in BmlifeSpider.visited:
                yield scrapy.Request(url_data)
            # print(url_data)

    def parse(self, response):
        print(response)

        print(response.url)
        self.visited.append(response.url)

        if 'json' in response.url:
            yield from self._parse_json(response)
        else:
            yield from self._parse_web(response)



