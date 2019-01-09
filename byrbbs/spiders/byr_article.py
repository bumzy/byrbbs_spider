# -*- coding: utf-8 -*-
import scrapy
from byrbbs.spiders.byr_config import URL_HEAD,HEADERS,LOGIN_FORMDATA
from scrapy.conf import settings
from byrbbs.items import ByrArticleItem
import pymongo
import re

class ByrArticleSpider(scrapy.Spider):
    pipeline = ['ByrArticlePipeline']
    name = "byr_article"
    allowed_domains = ["bbs.byr.cn"]
    start_urls = ["https://bbs.byr.cn"]
    article_per_list = 30

    def start_requests(self):
        return [scrapy.FormRequest("https://bbs.byr.cn/user/ajax_login.json",
                                   formdata=LOGIN_FORMDATA,
                                   meta={'cookiejar': 1},
                                   headers=HEADERS,
                                   callback=self.logged_in)]

    def logged_in(self, response):
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL_SECTION']]  # 获得collection的句柄

        # DB_CONFIG = {'host': '118.89.225.208', 'user': 'root', 'passwd': 'chen12//', 'db': 'byrbbs', 'port': 3306,
        #              'charset': 'utf8'}
        # conn = MySQLdb.connect(**DB_CONFIG)
        # cursor = conn.cursor()
        # sql = 'select * from section'
        # cursor.execute(sql)
        # for row in cursor.fetchall():
        for section in self.coll.find():
            item = ByrArticleItem()
            item['section_name'] = section['section_name']
            yield scrapy.Request(response.urljoin(section['section_url']),meta={'cookiejar':response.meta['cookiejar'],'item':item},headers=HEADERS, callback=self.parse_article_list_pre)

        # 用于测试指定板块或文章
        # self.start_urls = ['https://bbs.byr.cn/article/BM_Market/693']
        # self.start_url = [URL_HEAD+ r'/board/BM_Market']
        # item = ByrArticleItem()
        # item['section_name'] = 'BM_Market'
        # return scrapy.Request(self.start_url[0], meta={'cookiejar': response.meta['cookiejar'],'item':item}, headers=HEADERS, callback=self.parse_article_list_pre)


    # 处理列表，翻页问题
    def parse_article_list_pre(self, response):
        page_list_num = response.xpath('//*[@class="t-pre-bottom"]/div[1]/ul/li[1]/i/text()').extract()[0]
        total_num = int(page_list_num)/self.article_per_list+1  #页数从1到total_num
        first_list = response._get_url()
        for i in xrange(1,total_num+1):
            crawl_list_url = first_list+'?p='+str(i)
            yield scrapy.Request(crawl_list_url, meta={'cookiejar': response.meta['cookiejar'],'item':response.meta['item']}, headers=HEADERS,callback=self.parse_article_list)



    # 处理列表，获取列表上的每条文章信息与文章链接
    def parse_article_list(self, response):
        # print "parse_article_list "+response._get_url()
        section_name = response.meta['item']['section_name']
        sel_article = response.xpath('//*[@class="b-content"]/table/tbody/tr')
        article_url = sel_article.xpath('td[2]/a/@href').extract()
        article_title = sel_article.xpath('td[2]/a/text()').extract()
        article_createtime = sel_article.xpath('td[3]/text()').extract()
        article_author = sel_article.xpath('td[4]/a/text()').extract()
        article_comment = sel_article.xpath('td[5]/text()').extract()

        # 处理列表的每一行，即每一篇文章的信息，存入item
        for index, url in enumerate(article_url):
            item = ByrArticleItem()
            item['section_name'] = section_name
            item['article_title'] = article_title[index]
            item['article_url'] = response.urljoin(article_url[index])
            item['article_createtime'] = article_createtime[index]
            item['article_author'] = article_author[index]
            item['article_comment'] = article_comment[index]
            yield scrapy.Request(item['article_url'], meta={'cookiejar': response.meta['cookiejar'],'item': item}, headers=HEADERS,callback=self.parse_article_content)

    # 处理文章主体内容
    def parse_article_content(self, response):
        # from scrapy.shell import inspect_response
        # import sys
        # inspect_response(response, self)
        # sys.exit()
        # print response._get_url()
        # print response.body
        article = response.xpath('/html/body/div[3]/div/table/tr[2]/td[2]/div').extract()[0]
        article = re.sub('</?(font|div).*?>', '', article)
        article = re.sub('<br>', '\n', article)
        item = response.meta['item']
        item['article_content'] = article
        yield item


