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

        docList = response.xpath('//ul[@class="list"]/li')
        if (len(docList) > 0):
            for li in docList:
                item = LexisItem()
                item['title'] = li.xpath('./a/text()').extract()[0]
                item['href'] = li.xpath('./a/@href').extract()[0]

                yield item
        # print("！！！！！返回信息是：")
        # info = sites.xpath('./li')
        # # 从sites中我们再进一步获取到所有电影的所有信息
        # for i in info:  # 这里的i是每一部电影的信息
        #     # 排名
        #     num = i.xpath('./div//em[@class=""]//text()').extract()  # 获取到的为列表类型
        #     # extract()是提取器  将我们匹配到的东西取出来
        #     print(num[0], end=";")
        #     # 标题
        #     title = i.xpath('.//span[@class="title"]/text()').extract()
        #     print(title[0], end=";")
        #     # 评论
        #     remark = i.xpath('.//span[@class="inq"]//text()').extract()
        #     # 分数
        #     score = i.xpath('./div//span[@class="rating_num"]//text()').extract()
        #     print(score[0])

        # nextlink = response.xpath('//span[@class="next"]/link/@href').extract()

        # 还记得我们之前定义的url吗，由于电影太多网页有翻页显示，这里我们获取到翻页的那个按钮的连接nextlink
        # if nextlink:  # 翻到最后一页是没有连接的，所以这里我们要判断一下
        #     nextlink = nextlink[0]
        #     print(nextlink)
        #     yield Request(self.url + nextlink, callback=self.parse)
