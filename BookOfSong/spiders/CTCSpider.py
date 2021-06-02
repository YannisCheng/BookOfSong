import logging

from scrapy import Spider, Selector, Request
from BookOfSong.items import BOSItem


class CTCSpider(Spider):
    name = "CTC_BOS"
    allowed_domains = ["https://www.liuxue86.com/", "https://www.hao86.com/"]
    start_urls = ["https://www.liuxue86.com/a/3085448.html"]

    '''
    遍历诗经中的诗集
    '''

    def parse(self, response, **kwargs):
        first = Selector(response)
        node = first.xpath('//div[@class="main_zhengw"]/table/tbody/tr/td/a/@href')
        node_name = first.xpath('//div[@class="main_zhengw"]/table/tbody/tr/td/a/span/span/text()').extract()
        logging.debug(len(node))
        for item_name in node_name:
            logging.debug(item_name)
        for item in node:
            logging.debug(item.extract())
            yield Request(url=item.extract(), callback=self.parse_second,
                          dont_filter=True)
        # 此处设置的地址是各个辑的地址，该地址中包含着该辑下所有的篇目,替换此处的url时，需要更改parse_third#bosItem['bos_album'] = "小雅·荡之什"的值
        #yield Request(url="https://www.liuxue86.com/a/3085398.html", callback=self.parse_second,dont_filter=True)

    '''
    遍历单个诗集中的篇目
    '''

    def parse_second(self, response):
        logging.debug("----------------debug----------------")
        node = Selector(response)
        logging.debug(response.url)
        n_list = node.xpath('//div[@class="main_zhengw"]/p/a/@href').extract()
        logging.debug(len(n_list))
        for n_item in n_list:
            logging.debug(n_item)
            yield Request(url=n_item, callback=self.parse_third,
                          dont_filter=True)
        # yield Request(url="https://www.hao86.com/shici_view_9a407f43ac9a407f/", callback=self.parse_third,
        #               dont_filter=True)

    '''
    单个诗集中的具体诗文篇目内容
    '''

    def parse_third(self, response):
        bosItem = BOSItem()
        node = Selector(response)
        logging.debug(response.url)

        # 章
        bosItem['bos_album'] = ""

        # 名称
        node_name = node.xpath('//div[@class="jinyesi1"]/a/text()').extract()
        bosItem['bos_name'] = node_name[0]

        # 朝代
        node_chaodai = node.xpath('//div[@class="jinyesi"]/p/a[@class="zuozhechaodai"]/text()').extract()
        bosItem['bos_dynasty'] = node_chaodai[0]

        # 作者
        node_zuozhe = node.xpath('//div[@class="jinyesi"]/p/a[@class="zuozhe"]/text()').extract()
        bosItem['bos_author'] = node_zuozhe[0]

        # 拼音
        node_pinyin = node.xpath('//p[@class="jinysshici"]/span[@class="none-pinyin"]/text()').extract()
        pinyin_str = ""
        for content_item in node_pinyin:
            if content_item == '\n':
                node_pinyin.remove(content_item)
        for pinyin_item in node_pinyin:
            pinyin_str = pinyin_str + pinyin_item + '\n'
        bosItem['bos_pinyin'] = pinyin_str

        # 原文
        content_str = ""
        node_content = node.xpath('//p[@class="jinysshici"]/text()').extract()
        for content_item in node_content:
            if content_item == '\n                                                            ' \
                    or content_item == '\n                                            ' \
                    or content_item == '\n' \
                    or content_item == '                        \n' \
                    or content_item == ' \n':
                node_content.remove(content_item)

        for content_item in node_content:
            length = len(content_item)
            content_str = content_str + content_item[25:length] + "\n"
        bosItem['bos_content'] = content_str

        #print(bosItem)

        bosItem.save_to_res()
