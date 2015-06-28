# -*- coding: utf-8 -*-
import scrapy


class startPageSpider(scrapy.Spider):
    name = "startPageSpider"
    allowed_domains = ["aaa.com"]
    start_urls = (
        'http://www.aaa.com/',
    )

    def parse(self, response):
        pass
