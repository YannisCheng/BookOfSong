import logging

from scrapy import Spider, Selector, Request


# 《庄子》
class LaoZi(Spider):
    name = 'zz'
    allowed_domains = ['www.kulemi.com']
    start_urls = ['http://www.kulemi.com/31724/catalog/']

    def parse(self, response, **kwargs):
        # item = ZZTGItem()
        node = Selector(response)
        node_list = node.xpath('//ul[@class="catalog-list"]/li/a/@href').extract()
        node_name_list = node.xpath('//span/a/text()').extract()
        indexNum = 0
        for item_href in node_list:
            indexNum = indexNum + 1
            if indexNum < 5:
                logging.debug(item_href)
                yield Request(url=item_href, callback=self.second_parse, dont_filter=True)

    def second_parse(self, response):
        node = Selector(response)

        # 文章标题
        titles = node.xpath('//div[@class="chapter-head"]/h2/text()').extract()[0].split('·')
        # 辑名称
        logging.debug(titles[0].replace('\r', '').replace('\n', ''))
        # 篇目名称
        logging.debug(titles[1])

        # 字数
        charNum = node.xpath('//div[@class="chapter-head"]/div[@class="info"]/span/text()').extract()
        logging.debug(charNum[3].split('：')[0])
        logging.debug(charNum[3].split('：')[1])

        # 文章内容
        content_list = node.xpath('//div[@class="chapter-content"]/p/text()').extract()
        content_str = ""
        for content_item in content_list:
            # logging.debug(content_item)
            content_str = content_str + '\n' + content_item
        logging.debug(content_str)
