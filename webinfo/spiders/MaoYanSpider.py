import scrapy
from scrapy.http import Request
# from webinfo.items import LexisItem
from webinfo.items import MaoYanItem


class MaoYanSpider(scrapy.Spider):
    # 这个name是你必须给它一个唯一的名字  后面我们执行文件时的名字
    name = "maoyan"

    allowed_domains = ["maoyan.com"]

    # 这个列表中的url可以有多个，它会依次都执行，我们这里简单爬取一个
    start_urls = [
        "http://maoyan.com/films"
    ]

    custom_settings = {
        'ITEM_PIPELINES': {'webinfo.pipelines.EmptyPipeline': 300, }
    }

    def parse(self, response):  # 默认函数parse

        doc_list = response.xpath('//dl[@class="movie-list"]//dd')
        if (len(doc_list) > 0):
            for doc in doc_list:
                # item = MaoYanItem()
                item = {}
                item['src'] = doc.xpath('./div[@class="movie-item"]/a/div/img[1]/@src').extract()[0]
                item['title'] = doc.xpath('./div[contains(@class, "movie-item-title")]/a/text()').extract()[0]
                score = doc.xpath('./div[contains(@class, "channel-detail-orange")]//i')
                if (len(score) > 0):
                    integer = doc.xpath('./div[contains(@class, "channel-detail-orange")]/i[@class="integer"]/text()').extract()[0]
                    fraction = doc.xpath('./div[contains(@class, "channel-detail-orange")]/i[@class="fraction"]/text()').extract()[0]
                    item['score'] = integer + fraction
                else:
                    item['score'] = '暂无评分'
                yield item
                # print(item)
            next_page = response.xpath('//div[@class="movies-pager"]/ul[@class="list-pager"]//a[contains(text(), "下一页")]/@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
