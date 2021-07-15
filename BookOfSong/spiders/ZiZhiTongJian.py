import logging

from scrapy import Spider, Selector, Request

from BookOfSong.items import ZZTGItem


# 《资治通鉴》
class LaoZi(Spider):
    name = 'zztj_lock'
    allowed_domains = ['www.kulemi.com']
    start_urls = ['http://www.kulemi.com/zt/68/']

    def parse(self, response, **kwargs):
        node = Selector(response)
        node_list = node.xpath('//ul[@class="catalog"]/li/a/@href').extract()
        #node_name_list = node.xpath('//span/a/text()').extract()
        #indexNum = 0
        for item_href in node_list:
            #indexNum = indexNum + 1
            #if indexNum < 5:
            #    logging.debug(item_href)
            yield Request(url=item_href, callback=self.second_parse, dont_filter=True)

    def second_parse(self, response):
        node = Selector(response)
        item = ZZTGItem()

        titles = node.xpath('//div[@class="chapter-head"]/h2/text()').extract()[0].split('·')
        # 辑名称
        #logging.debug(titles[0].replace('\r', '').replace('\n', ''))
        item['album_name'] = titles[0].replace('\r', '').replace('\n', '')
        # 篇目名称
        #logging.debug(titles[1])
        item['title'] = titles[1]

        # 字数
        charNum = node.xpath('//div[@class="chapter-head"]/div[@class="info"]/span/text()').extract()
        #logging.debug(charNum[3].split('：')[0])
        #logging.debug(charNum[3].split('：')[1])
        item['author'] = '司马光'
        item['char_num'] = charNum[3].split('：')[1]

        # 文章内容
        content_list = node.xpath('//div[@class="chapter-content"]/p/text()').extract()
        content_str = ""
        for content_item in content_list:
            # logging.debug(content_item)
            content_str = content_str + '\n' + content_item
        # logging.debug(content_str)
        item['content'] = content_str
        item.save_to_es()
