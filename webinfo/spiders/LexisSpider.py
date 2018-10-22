import scrapy
from scrapy.http import Request
# from webinfo.items import LexisItem
from webinfo.items import LexisItem


class LexisSpider(scrapy.Spider):
    # 这个name是你必须给它一个唯一的名字  后面我们执行文件时的名字
    name = "lexis"

    allowed_domains = ["hk.lexiscn.com"]

    # 这个列表中的url可以有多个，它会依次都执行，我们这里简单爬取一个
    start_urls = [
        "http://hk.lexiscn.com/search/index?keyword=%E5%85%AC%E5%8F%B8%E6%B3%95"
    ]

    # 因为豆瓣250有翻页操作，我们设置这个url用来翻页
    # url = "https://movie.douban.com/top250"

    def parse(self, response):  # 默认函数parse

        doc_list = response.xpath('//ul[@class="list"]/li')
        if (len(doc_list) > 0):
            for li in doc_list:
                item = LexisItem()
                item['title'] = li.xpath('./a/text()').extract()[0]
                item['href'] = li.xpath('./a/@href').extract()[0]

                yield item
