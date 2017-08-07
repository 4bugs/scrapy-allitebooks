# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class DownloadItem(scrapy.Item):
    name = Field()
    Url = Field()


class BooksItem(scrapy.Item):
    url = Field()
    # 书名
    name = Field()
    # 简介
    brief_introduction = Field()
    # 书封面图url
    book_image_url = Field()
    author = Field()
    isbn = Field()
    year = Field()
    pages = Field()
    language = Field()
    file_size = Field()
    file_format = Field()
    category = Field()
    description = Field()
    download_links = Field()
