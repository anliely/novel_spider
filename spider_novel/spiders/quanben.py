import os
import scrapy
from spider_novel.items import NovelClassItem, NovelBookDirItem


class QuanbenSpider(scrapy.Spider):
    name = 'quanben'
    allowed_domains = ['quanben.io']
    start_urls = ['http://quanben.io/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "http://quanben.io"
        self.novel_class_list = []

    def parse(self, response):
        novel_class = response.xpath("/html/body/div[1]/a")
        for x in novel_class:
            novel_item = NovelClassItem()
            novel_item['title'] = x.xpath('span/text()').get()
            novel_item['url'] = self.base_url + x.xpath('@href').get()
            yield scrapy.Request(novel_item['url'], meta={'item': novel_item}, callback=self.dir_parse_page)

    def dir_parse_page(self, response):
        novel_item = response.meta['item']
        page_str = response.xpath("/html/body/div[3]/div[14]/p[2]/span/text()").get()
        page = int(page_str.split("/")[-1].replace(" ", ""))
        for x in range(0, page + 1):
            if x == 0:
                url = novel_item['url']
            else:
                new_url = novel_item['url'].split(".html")[0]
                url = f"{new_url}_{x}.html"
            yield scrapy.Request(url, meta={'item': novel_item}, callback=self.dir_parse, dont_filter=True)

    def dir_parse(self, response):
        item = response.meta['item']
        dir_list = response.xpath("/html/body/div[3]/div/div")

        for y in dir_list:
            item['book_name'] = y.xpath('h3/a/span/text()').get()
            item['author'] = y.xpath('p[1]/span/text()').get()
            item['content_list'] = []
            url = self.base_url + y.xpath('h3/a/@href').get()
            item['book_url'] = url
            url += "list.html"
            yield scrapy.Request(url, meta={'item': item}, callback=self.book_page_parse)

    def book_page_parse(self, response):
        item = response.meta['item']

        last_dir_str = response.xpath("/html/body/div[3]/ul[2]/li[23]/a[last()]/@href").get()
        last_dir = int(last_dir_str.split("/")[-1].split(".")[0])
        for x in range(1, last_dir + 1):
            yield scrapy.Request(f"{item['book_url']}{x}.html",
                                 meta={'item': item, 'dir_item': item, "page": x, 'total': last_dir + 1},
                                 callback=self.book_parse)

    def book_parse(self, response):
        item = response.meta['item']
        contents = response.xpath('//*[@id="content"]/p/text()')
        content_list = list()
        for content in contents:
            content_list.append(content.get())
        item['content_list'] = content_list
        return item
