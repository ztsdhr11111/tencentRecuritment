# -*- coding: utf-8 -*-
import scrapy
import re
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?start=0#a']

    def parse(self, response):
        item = TencentItem()
        items = response.xpath('//*[contains(@class,"odd") or contains(@class,"even")]')
        for i in items:
            item['name'] = i.xpath('./td[1]/a/text()').extract_first()
            item['detailLink'] = 'http://hr.tencent.com/' + i.xpath('./td[1]/a/@href').extract_first()
            item['positionInfo'] = i.xpath('./td[2]/text()').extract_first()
            item['peopleNumber'] = i.xpath('./td[3]/text()').extract_first()
            item['workLocation'] = i.xpath('./td[4]/text()').extract_first()
            item['publishTime'] = i.xpath('./td[5]/text()').extract_first()
            yield item

        now_page = int(re.search(r"\d+", response.url).group(0))
        print('*' * 20)
        if now_page < 216:
            url = re.sub(r"\d+", str(now_page + 10), response.url)
            print('this is next page url:%s' % url)
            print('*' * 100)
            yield scrapy.Request(url, callback=self.parse)