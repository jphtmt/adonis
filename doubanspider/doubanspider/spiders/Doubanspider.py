#!/usr/bin/env python
# encoding: utf-8

from scrapy.spider import BaseSpider
from scrapy.selector import Selector

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from doubanspider.items import DoubanspiderItem
from scrapy.http import Request,FormRequest

class doubanSpider(BaseSpider):
    name = "douban"
    allowed_domains = ['douban.com']
    start_urls = ['http://www.douban.com/']

    headers = {
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "accept-encoding":"gzip, deflate",
                "accept-language":"zh-CN,zh;q=0.8,en;q=0.6",
                "content-type":"application/x-www-form-urlencoded",
                "referer":"https://www.douban.com/accounts/login",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
                "Connection": "keep-alive"}












    def start_requests(self):
        return [Request('https://www.douban.com/accounts/login',
                        meta = {'cookiejar':1},
                        callback = self.post_login)]

    #headers = {
     #   "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
      #  "accept-encoding":"gzip, deflate",
       # "accept-language":"zh-CN,zh;q=0.8,en;q=0.6",
        #"content-type":"application/x-www-form-urlencoded",
       # "referer":"https://www.douban.com/accounts/login",
       # "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
       # "Connection": "keep-alive"



 #               }
#






    def post_login(self,response):
        print 'Preparing login'
        return [FormRequest.from_response(response,
                                          meta = {'cookiejar':response.meta['cookiejar']},
                                          headers = self.headers,
                                          formdata = {
                                              'source':'None',
                                              'form_email':'573980664@qq.com',
                                              'form_password':''},
                                                callback = self.parse_page,
                                                dont_filter = True)]


    def after_login(self,response):
        print 'after login '
        for url in self.start_urls:
            yield self.make_requests_from_url(url)


    def parse_page(self,response):
        print ' parse_page'
        sel = Selector(response)
       # sel.remove_namespaces()
        answer = sel.xpath('//*[@id="db-global-nav"]/div/div[1]/ul/li[2]/a/span[1]/text()').extract()
        item = DoubanspiderItem()
        item['loginName']=answer
        print item

        return item


