# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookofsongPipeline:
    def process_item(self, item, spider):
        # 执行items.py文件的save_to_es方法将数据写入elasticsearch搜索引擎
        item.save_to_es()
        return item
