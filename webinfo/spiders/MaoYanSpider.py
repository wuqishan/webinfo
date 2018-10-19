import scrapy
from scrapy.http import Request
# from webinfo.items import LexisItem
from webinfo.items import LexisItem


class LexisSpider(scrapy.Spider):
    # 这个name是你必须给它一个唯一的名字  后面我们执行文件时的名字
    name = "maoyan"

    allowed_domains = ["maoyan.com"]

    # 这个列表中的url可以有多个，它会依次都执行，我们这里简单爬取一个
    start_urls = [
        "http://maoyan.com/films"
    ]

    # 因为豆瓣250有翻页操作，我们设置这个url用来翻页
    # url = "https://movie.douban.com/top250"

    def parse(self, response):  # 默认函数parse

        docList = response.xpath('//ul[@class="list"]/li')
        if (len(docList) > 0):
            for li in docList:
                item = LexisItem()
                item['title'] = li.xpath('./a/text()').extract()[0]
                item['href'] = li.xpath('./a/@href').extract()[0]

                yield item


