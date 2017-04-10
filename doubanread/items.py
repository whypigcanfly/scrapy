# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanreadItem(scrapy.Item):
    # define the fields for your item here like:
    main_title = scrapy.Field()#书名
    sub_title = scrapy.Field()#副标题
    author = scrapy.Field()#作者
    type = scrapy.Field()#类型
    score = scrapy.Field()#评分
    describe = scrapy.Field()#简介
    detail_url = scrapy.Field()#详情链接

