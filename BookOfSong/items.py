# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# items.py,文件是专门用于:接收爬虫获取到的数据信息的，就相当于是容器文件。
# 设置爬虫获取到的信息容器类
from BookOfSong.spiders.ArticleType import ArticleType


class BOSItem(scrapy.Item):
    # 篇目名称
    bos_name = scrapy.Field()
    # 作者
    bos_author = scrapy.Field()
    # 朝代
    bos_dynasty = scrapy.Field()
    # 拼音
    bos_pinyin = scrapy.Field()
    # 内容
    bos_content = scrapy.Field()
    # 所在章节
    bos_album = scrapy.Field()

    def save_to_res(self):
        # 实例化elasticsearch(搜索引擎对象)
        article = ArticleType()
        # 字段名称=值
        article.album = self['bos_album']
        article.name = self['bos_name']
        article.author = self['bos_author']
        article.dynasty = self['bos_dynasty']
        article.pinyin = self['bos_pinyin']
        article.content = self['bos_content']
        # 将数据写入elasticsearch(搜索引擎对象)
        article.save()
        return
