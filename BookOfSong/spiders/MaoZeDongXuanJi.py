import logging

from scrapy import Spider, Selector, Request

from BookOfSong.items import MaoXuanItems


class MaoZeDongXuanJi(Spider):
    name = "mxj_lock"
    allowed_domains = ["http://ex.cssn.cn/"]
    start_urls = ["http://ex.cssn.cn/sjxz/xsjdk/mkszyjd/mzdsx/840200/"]
    #  {'./84020000/': '毛泽东选集第1卷', './84020001/': '毛泽东选集第2卷', './84020002/': '毛泽东选集第3卷', './84020003/': '毛泽东选集第4卷'}
    dict_mapping = dict()

    # 遍历选集
    def parse(self, response, **kwargs):
        node = Selector(response)
        # div[@class="f-main-left-sire"]/div[@class="f-main-left"]/
        album_list_title = node.xpath(
            '//div[@class="f-main-leftMain-content clear"]/div[@class="ImageListView"]/ol/li/a/text()').extract()
        album_list_url = node.xpath(
            '//div[@class="f-main-leftMain-content clear"]/div[@class="ImageListView"]/ol/li/a/@href').extract()

        for album_item_title, album_item_url in zip(album_list_title, album_list_url):
            self.dict_mapping[album_item_url] = album_item_title
            le = len(album_item_url)
            yield Request(url=response.url + album_item_url[2:le], callback=self.second_parse, dont_filter=True)

    # 遍历卷
    def second_parse(self, response):
        node = Selector(response)
        juan_list_url = node.xpath(
            '//div[@class="f-main-leftMain-content clear"]/div[@class="ImageListView"]/ol/li/a/@href').extract()
        juan_list_title = node.xpath(
            '//div[@class="f-main-leftMain-content clear"]/div[@class="ImageListView"]/ol/li/a/text()').extract()

        # ./201311/t20131124_876414.shtml
        # http://ex.cssn.cn/sjxz/xsjdk/mkszyjd/mzdsx/840200/84020000/201311/t20131124_876414.shtml
        for juan_item_url in juan_list_url:
            if juan_item_url != './201311/t20131124_876415.shtml':
                le = len(juan_item_url)
                yield Request(url=response.url + juan_item_url[2:le],
                              callback=self.third_parse, dont_filter=True)

    def third_parse(self, response):
        item = MaoXuanItems()
        node = Selector(response)

        # 卷
        item['album'] = self.dict_mapping['./' + response.url[50:58] + '/']
        title = node.xpath(
            '//div[@class="f-main-left"]/div[@class="f-main-left-Title"]/span/text()').extract()[0]
        # logging.debug(title)

        # 标题
        item['title'] = title

        # 作者
        item['author'] = '毛泽东'

        # 内容
        content = node.xpath(
            '//div[@class="f-main-left"]/div[@class="f-main-leftMain-content clear"]/p/text()').extract()
        # logging.debug(content)

        content_str = ""
        for content_item in content:
            if content_item != '责任编辑：丁冬勤':
                content_str = content_str + content_item

        item['content'] = content_str
        item.save_to_es()
        # logging.debug(content_str)
