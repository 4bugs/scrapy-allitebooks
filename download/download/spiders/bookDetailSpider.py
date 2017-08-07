# -*- coding: utf-8 -*-
import scrapy
import pymongo

from ..settings import proxy
from ..items import BooksItem
import time

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "itbooks"

class BookdetailspiderSpider(scrapy.Spider):
    name = "bookDetailSpider"
    allowed_domains = ["allitebooks.com"]
    start_urls = (
        'http://www.allitebooks.com/top-down-network-design-3rd-edition/',
    )

    def start_requests(self):
        conn = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
        db = conn[MONGODB_DB]
        # urls = list(db.urls.find({}, {'Url':1, '_id':0}).limit(10))
        urls = list(db.urls.find({}, {'Url': 1, '_id': 0}))
        for url in urls:
            yield scrapy.Request(
                url=url["Url"],
                meta={
                    "proxy":proxy,
                },
                callback=self.parse
            )

    def parse(self, response):
        item = BooksItem()
        item["url"] = response.url
        item["name"] = response.xpath('//*[@class="single-title"]/text()').extract()
        item["brief_introduction"] = response.xpath('//*[@class="entry-header"]/h4/text()').extract()
        item["book_image_url"] = response.xpath('//*[@class="entry-body-thumbnail hover-thumb"]/a/img/@src').extract()
        book_detail = response.xpath('//*[@class="book-detail"]/dl/dd/text()').extract()
        item["author"] = response.xpath('//*[@class="book-detail"]/dl/dd/a/text()').extract()[0]
        item["isbn"] = book_detail[1]
        item["year"] = book_detail[2]
        item["pages"] = book_detail[3]
        item["language"] = book_detail[4]
        item["file_size"] = book_detail[5]
        item["file_format"] = book_detail[6]
        item["category"] = response.xpath('//*[@class="book-detail"]/dl/dd/a/text()').extract()[1]
        item["download_links"] = response.xpath('//span[@class="download-links"]/a/@href').extract()[0].replace(" ", "%20")
        yield item