from scrapy import Spider, Selector

from BookOfSong.items import LaoZiItems


# 《老子-帛书》
class LaoZi(Spider):
    name = 'lz_lock'
    allowed_domains = ['http://www.guoxue123.com/']
    start_urls = ['http://www.guoxue123.com/zhibu/0101/03lzbs/004.htm']

    def parse(self, response, **kwargs):
        item = LaoZiItems()
        node = Selector(response)
        node_list = node.xpath('//td/p/text()').extract()
        content_list = list()

        for index, node_item in enumerate(node_list):
            item['book_item'] = ""
            item['content'] = node_item
            content_list.append(item)
            # print(item)
            item.save_to_es()
