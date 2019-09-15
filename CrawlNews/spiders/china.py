# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['https://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow=r'article.*?\.html',
                restrict_xpaths="//div[@id='left_side']/div[@class='con_item']"),callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths="//div[@id='pageStyle']/a[text()='下一页']"))
    )


    def parse_item(self, response):
        item = {}
        item['title'] = response.xpath("//h1[@id='chan_newsTitle']/text()").extract_first()
        item['time'] = response.xpath("//div[@id='chan_newsInfo']/text()").re_first('(\d+-\d+-\d+\s\d+:\d+:\d+)')
        item['from'] = response.xpath("//div[@id='chan_newsInfo']/text()").re_first('来源：(.*)').strip()
        item['content'] = ''.join(response.xpath("//div[@id='chan_newsDetail']//text()").extract()).strip()
        item['url'] = response.url
        yield item

