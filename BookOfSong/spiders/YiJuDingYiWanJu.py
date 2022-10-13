import logging

from scrapy import Spider, Selector, Request


# 《一句顶一万句》


class YiJuDingYiWanJu(Spider):
    name = 'yjdywj'
    allowed_domains = ['www.tianyashuku.com']
    start_urls = ['https://www.tianyashuku.com/xdwx/6309/']

    def parse(self, response, **kwargs):
        node = Selector(response)
        node_list = node.xpath('//div[@class="book-list mb clearfix"]/ul/li/a/@href').extract()
        # yield Request(url='https://www.tianyashuku.com/xdwx/6309/280880.html', callback=self.second_parse, dont_filter=True)
        for item_href in node_list:
            logging.debug(item_href)
            yield Request(url='https://www.tianyashuku.com' + item_href, callback=self.second_parse, dont_filter=True)

    def second_parse(self, response):
        node = Selector(response)
        #     item = ShiJiItem()

        # 卷：卷一
        juanIndex = node.xpath('//head/title/text()').extract()
        logging.debug(juanIndex[0][6:13])

        # 文章标题：第一章
        title = node.xpath(
            '//article[@class="post clearfix"]/header[@class="post-header clearfix"]/h1[@class="post-title"]/text()').extract()
        logging.debug(title[0])

        # 内容
        content = node.xpath('//article[@class="post clearfix"]/div[@class="mb2"]/p/text()').extract()
        contentAll = ''
        for conItem in content:
            contentAll = contentAll + conItem + '\n'
        logging.debug(contentAll)
