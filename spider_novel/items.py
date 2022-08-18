# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelBookDirItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    book_url = scrapy.Field()
    content_list = scrapy.Field()


# class NovelClassItem:
#     title: str
#     url: str
#     book_list: list


class NovelClassItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    book_name = scrapy.Field()
    author = scrapy.Field()
    content_list = scrapy.Field()
    book_url = scrapy.Field()
