import logging

from scrapy import Spider, Selector, Request


class TangShiSanBai(Spider):
    name = "tasb"
    allowed_domains = ["http://www.300tangshi.com/"]
    start_urls = ["http://www.300tangshi.com/"]
    album_list = list()


    def parse(self, response, **kwargs):
        node = Selector(response)
        self.album_list = node.xpath('//div[@class="content-list clearfix"]/h2/text()').extract()

        node_list = node.xpath('//div[@class="content-list clearfix"]/ul[@class="clearfix"]/li/a/text()').extract()
        node_url_list = node.xpath('//div[@class="content-list clearfix"]/ul[@class="clearfix"]/li[@class="col-md-3"]/a/@href').extract()

        for node_item in node_list:
            logging.debug(node_item)
            # yield Request(url="http://www.ningyangtv.cn" + node_item, callback=self.second_parse, dont_filter=True)
        yield Request(url="http://www.ningyangtv.cn/bookview/224.html", callback=self.second_parse, dont_filter=True)