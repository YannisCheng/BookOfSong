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
            yield Request(url=baseUrl+item_href, callback=self.second_parse, dont_filter=True)

    def second_parse(self, response):
        node = Selector(response)
    #     item = ShiJiItem()
    #
        juanIndexs = node.xpath('//div[@class="book_middle_title"]/text()').extract()
        # 卷：卷一
        juanIndex = juanIndexs[3][2:]
        # 文章标题：耳中人
        title = node.xpath('//div[@class="book_middle_text"]/dl/dt/text()').extract()[0]
        logging.debug(title)
        # 内容
        content = node.xpath('//div[@class="book_middle_text"]/dl/dd/text()').extract()
        for conItem in content:
            logging.debug('item: '+conItem)

    #     # 辑名称
    #     #logging.debug(titles[0].replace('\r', '').replace('\n', ''))
    #     item['album_name'] = titles[0].replace('\r', '').replace('\n', '')
    #     # 篇目名称
    #     #logging.debug(titles[1])
    #     item['title'] = titles[1]
    #
    #     # 字数
    #     charNum = node.xpath('//div[@class="chapter-head"]/div[@class="info"]/span/text()').extract()
    #     #logging.debug(charNum[3].split('：')[0])
    #     #logging.debug(charNum[3].split('：')[1])
    #     item['char_num'] = charNum[3].split('：')[1]
    #     item['author'] = '司马迁'
    #
    #     # 文章内容
    #     content_list = node.xpath('//div[@class="chapter-content"]/p/text()').extract()
    #     content_str = ""
    #     for content_item in content_list:
    #         # logging.debug(content_item)
    #         content_str = content_str + '\n' + content_item
    #     #logging.debug(content_str)
    #     item['content'] = content_str
    #     item.save_to_es()
