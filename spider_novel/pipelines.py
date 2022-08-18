# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from spider_novel.items import NovelClassItem


class SpiderNovelPipeline:
    def process_item(self, item, spider):
        self.show_book(item, item['book_name'])
        return item

    def check_dir(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def show_book(self, book: NovelClassItem, title):
        dirname = f"novel/{book['title']}/{title}"
        self.check_dir(dirname)
        content_str = ""
        for y in book['content_list']:
            content_str += f"{y}\n"
        with open(f"{dirname}/{book['content_list'][0]}.txt", 'w') as f:
            f.write(content_str)
