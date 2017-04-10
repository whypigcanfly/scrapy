# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class DoubanreadPipeline(object):
    def process_item(self, item, spider):
        return item


#编码为utf8
class EncodeToUtf8Pipeline(object):

    def process_item(self, item, spider):
        for key in item.keys():
            item[key] = item[key].encode("utf-8")
        return item


#写入文件
class WriteToFilePipeline(object):

    def __init__(self):
        self.fp = open("douban.jl", "wb")

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) +"\n"
        self.fp.write(line)
        return item

    def close_spider(self, spider):
        print "==================="
        self.fp.close()


#写入数据库
class WriteToDataBasePipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    #pipeline默认调用
    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self._conditional_insert,item)#调用插入的方法
        query.addErrback(self._handle_error,item,spider)#调用异常处理方法
        return item

    def _conditional_insert(self,tx,item):
        #print item['name']
        sql="insert into doubanread(maintitle, subtitle, author, type, score, detail_url, `describe`) " \
            "values(%s,%s,%s, %s, %s, %s, %s )"
        params=(item["main_title"],item["sub_title"], item["author"], item["type"], item["score"],
                item["detail_url"], item["describe"])
        tx.execute(sql,params)

    #错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue

    @classmethod
    def from_settings(cls,settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams=dict(
            host=settings['MYSQL_HOST'],#读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',#编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool=adbapi.ConnectionPool('MySQLdb',**dbparams)#**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)#相当于dbpool付给了这个类，self中可以得到


def close_spider(self, spider):
    print "==================="
