import logging

from scrapy import Spider, Selector, Request

from BookOfSong.items import GGGZItem

'''
《古文观止》
'''
class GuWenGuanZhi(Spider):
    name = "gggz_lock"
    allowed_domains = ["https://www.zggdwx.com/"]
    start_urls = ["https://www.zggdwx.com/guwen.html"]

    ji_num = list()
    ji_name = list()

    def parse(self, response, **kwargs):
        node_top = Selector(response)
        node_list = node_top.xpath(
            '//div[@class="directory"]/div[@class="mdui-list"]/div[@class="mdui-subheader"]/text()').extract()
        node_list_url = node_top.xpath(
            '//div[@class="directory"]/div[@class="mdui-list"]/a[@class="mdui-list-item mdui-ripple"]/@href').extract()
        for node_item in node_list:
            node_item_list = node_item.split()
            self.ji_num.append(node_item_list[0])
            self.ji_name.append(node_item_list[1])

        for node_item_url in node_list_url:
            logging.debug(node_item_url)
            yield Request(url=node_item_url, callback=self.second_parse, dont_filter=True)

    def second_parse(self, response):
        item = GGGZItem()

        global author
        album_index = ''
        album_name = ''

        logging.debug('------------->>>>>>>>>>>> ------------------>>>>>>>>>>>')
        logging.debug(response.url)
        # 文章所在index
        url_index = int(response.url[29:len(response.url) - 5])
        logging.debug(url_index)

        content_node = Selector(response)

        if url_index in range(1, 9):
            album_index = self.ji_num[0]
            album_name = self.ji_name[0]
        elif url_index in range(10, 14):
            album_index = self.ji_num[1]
            album_name = self.ji_name[1]
        elif url_index in range(15, 23):
            album_index = self.ji_num[2]
            album_name = self.ji_name[2]
        elif url_index in range(24, 34):
            album_index = self.ji_num[3]
            album_name = self.ji_name[3]
        elif url_index in range(35, 47):
            album_index = self.ji_num[4]
            album_name = self.ji_name[4]
        elif url_index in range(48, 60):
            album_index = self.ji_num[5]
            album_name = self.ji_name[5]
        elif url_index in range(61, 85):
            album_index = self.ji_num[6]
            album_name = self.ji_name[6]
        elif url_index in range(86, 101):
            album_index = self.ji_num[7]
            album_name = self.ji_name[7]
        elif url_index in range(102, 117):
            album_index = self.ji_num[8]
            album_name = self.ji_name[8]
        elif url_index in range(118, 129):
            album_index = self.ji_num[9]
            album_name = self.ji_name[9]
        elif url_index in range(130, 143):
            album_index = self.ji_num[10]
            album_name = self.ji_name[10]
        elif url_index in range(144, 175):
            album_index = self.ji_num[11]
            album_name = self.ji_name[11]

        # logging.debug(album_index)
        # logging.debug(album_name)

        item['album_index'] = album_index
        item['album_name'] = album_name
        # 文章标题
        title = content_node.xpath(
            '//div[@class="mdui-container-fluid wrapper"]/div[@class="mdui-card mdui-card-shadow mdui-typo"]/h1/text()').extract()
        # logging.debug(title[0])
        item['title'] = title[0]

        # 文章内容
        content = content_node.xpath(
            '//div[@class="mdui-container-fluid wrapper"]/div[@class="mdui-card mdui-card-shadow mdui-typo"]/p/text()').extract()
        content_str = ""
        for content_item in content:
            content_str = content_str + "    " + content_item
        # logging.debug(content_str)
        item['content'] = content_str

        # 作者1
        author1 = content_node.xpath(
            '//div[@class="mdui-container-fluid wrapper"]/div[@class="mdui-card mdui-card-shadow mdui-typo"]/b/text()').extract()
        # 作者2
        author2 = content_node.xpath(
            '//div[@class="mdui-container-fluid wrapper"]/div[@class="mdui-card mdui-card-shadow mdui-typo"]/b/a/text()').extract()

        if len(author2) != 0:
            author = author1[0] + author2[0]
        elif len(author1) != 0:
            author = author1[0]
        else:
            author = ''
        # logging.debug(author)
        item['author'] = author
        item.save_to_es()
