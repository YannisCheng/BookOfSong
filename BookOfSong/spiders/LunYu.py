import logging

from scrapy import Spider, Selector, Request

from BookOfSong.items import LaoZiItems, LunYuItems

'''
《论语》
'''


class LunYu(Spider):
    name = 'ly_lock'
    allowed_domains = ['https://so.gushiwen.org/']
    start_urls = ['https://so.gushiwen.org/guwen/book_2.aspx']

    def parse(self, response, **kwargs):
        node = Selector(response)
        node_list = node.xpath(
            '//div[@class="main3"]/div[@class="left"]/div[@class="sons"]/div[@class="bookcont"]/ul/span/a/@href').extract()
        for node_item in node_list:
            logging.debug(node_item)
            yield Request(url=node_item, callback=self.second_parse, dont_filter=True)
        # yield Request(url="https://so.gushiwen.org/guwen/bookv_46653FD803893E4F699E8628DEAEE3C0.aspx",
        #               callback=self.second_parse, dont_filter=True)

    def second_parse(self, response):
        num = response.url[36:(len(response.url) - 5)]
        item = LunYuItems()
        node = Selector(response)
        str_xpath = '//div[@class="main3"]/div[@class="left"]/div[@class="sons"]/div[@id="cont' + num + '"]'
        title=node.xpath(str_xpath + '/h1/span/b/text()').extract()[0]
        right = len(title)-3
        item['album_name'] = title[0:right]
        item['author'] = '孔子'

        content = node.xpath(str_xpath + '/div[@class="contson"]/p/text()').extract()
        # logging.debug(item)
        for content_item in content:
            item['content'] = content_item
            # logging.debug(item)
            item.save_to_es()
