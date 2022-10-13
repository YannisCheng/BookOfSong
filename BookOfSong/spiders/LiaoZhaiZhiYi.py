import logging

from scrapy import Spider, Selector, Request


# 《聊斋志异》
# from BookOfSong.items import ShiJiItem


class LiaoZhaiZhiYi(Spider):
    name = 'lzzy'
    allowed_domains = ['ab.newdu.com']
    start_urls = ['http://ab.newdu.com/book/b35.html']

    def parse(self, response, **kwargs):
        baseUrl = 'http://ab.newdu.com'
        node = Selector(response)
        node_list = node.xpath('//div[@class="book_article_listtext"]/dl[@id="chapterlist"]/dd/a/@href').extract()
        for item_href in node_list[1:2:1]:
            yield Request(url='http://ab.newdu.com/book/s945.html', callback=self.second_parse, dont_filter=True)

    def second_parse(self, response):
        node = Selector(response)
    #     item = ShiJiItem()
    #
        juanIndexs = node.xpath('//div[@class="book_middle_title"]/text()').extract()
        # 卷：卷一
        juanIndex = juanIndexs[3][2:]
        # 文章标题：耳中人
        title = node.xpath('//div[@class="book_middle_text"]/dl/dt/text()').extract()[0]
        logging.debug('title: ' + title)
        # 内容
        content = node.xpath('//div[@class="book_middle_text"]/dl/dd/text()').extract()
        contentAll = ''
        for conItem in content:
            contentAll = contentAll+conItem
        logging.debug( contentAll)
