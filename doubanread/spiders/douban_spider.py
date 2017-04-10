#coding:UTF-8


import scrapy
from scrapy.http import Request
from doubanread.items import DoubanreadItem

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = [
        "https://read.douban.com/kind/0?start=0&sort=hot&promotion_only=False&min_price=None&max_price=None",
        "https://read.douban.com/kind/0?start=9990&sort=hot&promotion_only=False&min_price=None&max_price=None",
        "https://read.douban.com/kind/0?start=40&sort=hot&promotion_only=False&min_price=None&max_price=None",
        "https://read.douban.com/kind/0?start=60&sort=hot&promotion_only=False&min_price=None&max_price=None",
    ]

    custom_settings = {
        "ITEM_PIPELINES":{
            'doubanread.pipelines.EncodeToUtf8Pipeline': 300,
            #'doubanread.pipelines.WriteToFilePipeline': 800,
            # 'doubanread.pipelines.WriteToDataBasePipeline': 900,
        },
        "AUTOTHROTTLE_ENABLED":True,
        # The initial download delay
        "AUTOTHROTTLE_START_DELAY": 5,
        # The maximum download delay to be set in case of high latencies
        "AUTOTHROTTLE_MAX_DELAY" : 60,
        # The average number of requests Scrapy should be sending in parallel to
        # each remote server
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1.0,
        # Enable showing throttling stats for every response received:
        "AUTOTHROTTLE_DEBUG": False,
        "DOWNLOAD_DELAY":10,

    }

    headers = {
        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        "Accept-Encoding":"gzip, deflate, sdch, br",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Host":"read.douban.com",
        "Referer":"https://read.douban.com/kind/0?start=40&sort=hot&promotion_only=False&min_price=None&max_price=None",
        "Upgrade-Insecure-Requests":1,
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76 Safari/537.36"
    }

    def start_requests(self):
        # for url in self.start_urls:
        #     yield Request(url,dont_filter=True,headers=self.headers)
        for nu in xrange(0, 9100, 20):
            url = "https://read.douban.com/kind/0?start={page}&sort=hot&promotion_only=False&min_price=None&max_price=None".format(page=nu)
            yield Request(url, dont_filter=True, headers=self.headers)

    def parse(self, response):
        for sel in response.xpath("//li[@class='item store-item']"):
            item = DoubanreadItem()
            title_lsit = sel.xpath("div[@class='info']/div[@class='title']/a/text()").extract()
            item["main_title"] = title_lsit[0] if len(title_lsit)>0 else ""
            sub_title_list =  sel.xpath("div[@class='info']/div[@class='title']/p/text()").extract()
            item["sub_title"] = sub_title_list[0] if len(sub_title_list)>0 else ""
            author_list = sel.xpath("div[@class='info']/p/span/span[@class='labeled-text']/a[@class='author-item']/text()").extract()
            item["author"] = author_list[0] if len(author_list)>0 else ""
            type_list =  sel.xpath("div[@class='info']/p//span/span[@class='labeled-text']/span[@itemprop='genre']/text()").extract()
            item["type"] = ",".join(type_list)
            score_list =  sel.xpath("div[@class='info']/div[@class='rating list-rating']/span[@class='rating-average']/text()").extract()
            item["score"] = score_list[0] if len(score_list)>0 else ""
            desc_list =  sel.xpath("div[@class='info']/div[@class='article-desc-brief']/text()").extract()
            item["describe"] = desc_list[0] if len(desc_list)>0 else ""
            book_tmp =  sel.xpath("div[@class='info']/div[@class='title']/a/@href").extract()
            item["detail_url"] = ("https://read.douban.com"+book_tmp[0]) if len(book_tmp)>0 else ""
            yield item