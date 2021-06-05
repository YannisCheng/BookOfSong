# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# items.py,文件是专门用于:接收爬虫获取到的数据信息的，就相当于是容器文件。
# 设置爬虫获取到的信息容器类
from BookOfSong.spiders.es_mapping.ArticleTypeMaoXuan import ArticleTypeMaoXuan
from BookOfSong.spiders.es_mapping.ArticleTypeShiJing import ArticleType
from BookOfSong.spiders.es_mapping.ArticleTypeGGGZ import ArticleTypeGGGZ
from BookOfSong.spiders.es_mapping.ArticleTypeLaoZi import ArticleTypeLaoZi
from BookOfSong.spiders.es_mapping.ArticleTypeLunYu import ArticleTypeLunYu
from BookOfSong.spiders.es_mapping.ArticleTypeSGZ import ArticleTypeSGZ
from BookOfSong.spiders.es_mapping.ArticleTypeTangShi import ArticleTypeTangShi
from BookOfSong.spiders.es_mapping.ArticleTypeZhouYi import ArticleTypeZhouYi

'''
《诗经》
'''


class ShiJingItem(scrapy.Item):
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


'''
《古文观止》
'''


class GGGZItem(scrapy.Item):
    # 篇目名称
    album_index = scrapy.Field()
    album_name = scrapy.Field()
    title = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 内容
    content = scrapy.Field()

    def save_to_es(self):
        # 实例化elasticsearch(搜索引擎对象)
        article = ArticleTypeGGGZ()
        # 字段名称=值
        article.album_index = self['album_index']
        article.album_name = self['album_name']
        article.title = self['title']
        article.author = self['author']
        article.content = self['content']
        # 将数据写入elasticsearch(搜索引擎对象)
        article.save()
        return


'''
三国志
'''


class SGZItems(scrapy.Item):
    # 辑
    book_item_name = scrapy.Field()
    # 篇目名称
    book_item_name_title = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 内容
    content = scrapy.Field()

    def save_to_es(self):
        # 实例化elasticsearch(搜索引擎对象)
        article = ArticleTypeSGZ()
        # 字段名称=值
        article.book_item_name = self['book_item_name']
        article.book_item_name_title = self['book_item_name_title']
        article.author = self['author']
        article.content = self['content']
        # 将数据写入elasticsearch(搜索引擎对象)
        article.save()
        return


'''
老子-帛书
'''


class LaoZiItems(scrapy.Item):
    # 辑
    book_item = scrapy.Field()
    # 内容
    content = scrapy.Field()

    def save_to_es(self):
        # 实例化elasticsearch(搜索引擎对象)
        article = ArticleTypeLaoZi()
        # 字段名称=值
        article.book_item = self['book_item']
        article.content = self['content']
        # 将数据写入elasticsearch(搜索引擎对象)
        article.save()
        return


'''
《论语》
'''


class LunYuItems(scrapy.Item):
    # 篇目名称
    album_name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 内容
    content = scrapy.Field()

    def save_to_es(self):
        # 实例化elasticsearch(搜索引擎对象)
        article = ArticleTypeLunYu()
        # 字段名称=值
        article.album_name = self['album_name']
        article.author = self['author']
        article.content = self['content']
        # 将数据写入elasticsearch(搜索引擎对象)
        article.save()
        return



'''
《周易》
'''


class ZhouYiItems(scrapy.Item):
    # 辑
    book_item = scrapy.Field()
    # 内容
    content = scrapy.Field()

    def save_to_es(self):
        # 实例化elasticsearch(搜索引擎对象)
        article = ArticleTypeZhouYi()
        # 字段名称=值
        article.book_item = self['book_item']
        article.content = self['content']
        # 将数据写入elasticsearch(搜索引擎对象)
        article.save()
        return


'''
《唐诗三百首》
'''


class TangShiSanBaiItems(scrapy.Item):

    # 辑
    album_item = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 朝代
    density = scrapy.Field()
    # 名称
    title = scrapy.Field()
    # 诗体
    body = scrapy.Field()
    # 押韵字
    yun = scrapy.Field()
    # 内容
    content = scrapy.Field()

    def save_to_es(self):
        # 实例化elasticsearch(搜索引擎对象)
        article = ArticleTypeTangShi()
        # 字段名称=值
        article.album_item = self['album_item']
        article.author = self['author']
        article.density = self['density']
        article.title = self['title']
        article.body = self['body']
        article.yun = self['yun']
        article.content = self['content']
        # 将数据写入elasticsearch(搜索引擎对象)
        article.save()
        return

'''
《毛泽东选集》
'''


class MaoXuanItems(scrapy.Item):

    album = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()

    def save_to_es(self):
        # 实例化elasticsearch(搜索引擎对象)
        article = ArticleTypeMaoXuan()
        # 字段名称=值
        article.album = self['album']
        article.title = self['title']
        article.author = self['author']
        article.content = self['content']
        # 将数据写入elasticsearch(搜索引擎对象)
        article.save()
        return