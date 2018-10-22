import scrapy
from scrapy.mail import MailSender
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

            mailer = MailSender.from_settings(self.settings)
            # print(spider.settings)
            mailer.send(to=["1174955828@qq.com"], subject="Some subject", body="Some body", cc=[])

    def closed(self, reason):  # 爬取结束的时候发送邮件
        from scrapy.mail import MailSender

        # mailer = MailSender.from_settings(settings)# 出错了，没找到原因
        mailer = MailSender(
            smtphost="smtp.163.com",  # 发送邮件的服务器
            mailfrom="***********@163.com",  # 邮件发送者
            smtpuser="***********@163.com",  # 用户名
            smtppass="***********",  # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
            smtpport=25  # 端口号
        )
        body = u"""
        发送的邮件内容
        """
        subject = u'发送的邮件标题'