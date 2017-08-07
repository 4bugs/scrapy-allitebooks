# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import DownloadItem
import time
from ..settings import proxy


class BookspiderSpider(CrawlSpider):
    name = 'bookSpider'
    allowed_domains = ['http://www.allitebooks.com/']
    start_urls = ['http://www.allitebooks.com/']

    rules = (
        Rule(LinkExtractor(allow=r'page/%d'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        for p in range(723):
            yield scrapy.Request(
                url="http://www.allitebooks.com/page/%d/" % (p+1),
                meta={
                    "proxy": proxy,
                },
                callback=self.parse_item,
            )

    # def start_requests(self):
    #     yield scrapy.Request(
    #         url="http://www.allitebooks.com/page/598/",
    #         meta={
    #             "proxy": proxy,
    #         },
    #         callback=self.parse_item,
    #     )

    def parse_item(self, response):
        time.sleep(2)
        i = DownloadItem()
        names = response.xpath('//*[@class="entry-title"]/a/text()').extract()
        bookUrls = response.xpath('//*[@class="entry-title"]/a/@href').extract()
        bookNums = len(names)
        for k in range(bookNums):
            i["name"] = names[k]
            i["Url"] = bookUrls[k]
            yield i