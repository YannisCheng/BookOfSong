import logging

from scrapy import Spider, Selector, Request

from BookOfSong.items import ZhouYiItems


class ZhouYi(Spider):
    name = "zy"
    allowed_domains = ["http://www.ningyangtv.cn/"]
    start_urls = ["http://www.ningyangtv.cn/bookindex/13.html"]

    def parse(self, response, **kwargs):
        node = Selector(response)
        node_list = node.xpath('//div[@class="left"]/div[@class="article"]/dl[@class="book"]/ul/li/a/@href').extract()
        for node_item in node_list:
            logging.debug(node_item)
            yield Request(url="http://www.ningyangtv.cn"+node_item,callback=self.second_parse,dont_filter=True)
        # yield Request(url="http://www.ningyangtv.cn/bookview/224.html", callback=self.second_parse, dont_filter=True)

    def second_parse(self,response):
        item = ZhouYiItems()
        node = Selector(response)
        title = node.xpath('//div[@class="article"]/h2/text()').extract()[0]

        logging.debug(title[4:len(title)-2])
        item['book_item'] = title[4:len(title)-2]
        content = node.xpath('//div[@class="article"]/dl/dd[@id="cc"]/text()').extract()
        content_str = ''
        for content_item in content:
            content_str = content_str+content_item
        logging.debug(content_str)
        item['content'] = content_str
        item.save_to_es()