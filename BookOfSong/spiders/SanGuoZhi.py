import logging

from scrapy import Spider, Selector, Request

from BookOfSong.items import SGZItems

'''
《三国志》
'''


class SanGuoZhi(Spider):
    name = "sgz"
    allowed_domains = ["https://www.gushiwen.com/"]
    start_urls = ["https://www.gushiwen.com/dianji/54.html"]
    title_dict = dict()

    def parse(self, response, **kwargs):
        node = Selector(response)

        # 创建 [index：卷名] 字典
        node_url = node.xpath('//div[@id="bj"]/div[@id="main"]/div[@class]/a/@href').extract()
        for index, node_item_url in enumerate(node_url):
            if index <= 29:
                self.title_dict["https://www.gushiwen.com" + node_item_url] = "魏书"
            elif 30 <= index <= 44:
                self.title_dict["https://www.gushiwen.com" + node_item_url] = "蜀书"
            elif 45 <= index:
                self.title_dict["https://www.gushiwen.com" + node_item_url] = "吴书"
        # print(self.title_dict)
        for node_item_url2 in node_url:
            yield Request(url="https://www.gushiwen.com" + node_item_url2, callback=self.parse_second, dont_filter=True)
        # yield Request(url="https://www.gushiwen.com/dianjiv/77887.html", callback=self.parse_second,dont_filter=True)

    def parse_second(self, response):
        item = SGZItems()
        node = Selector(response)

        # 国号
        item['book_item_name'] = self.title_dict[response.url]

        # 作者
        item['author'] = "陈寿"

        # 文章标题
        item['book_item_name_title'] = node.xpath('//div[@id="bj"]/h1/text()').extract()[0]

        # 文章内容
        content_str = ""
        node_content = node.xpath('//div[@id="bj"]/div[@class="dianjiv"]/p/text()').extract()
        for node_content_item in node_content:
            content_str = content_str + node_content_item

        item['content'] = content_str
        item.save_to_es()
