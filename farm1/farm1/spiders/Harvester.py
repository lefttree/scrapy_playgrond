# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from farm1.items import Farm1Item


class HarvesterSpider(CrawlSpider):
    name = "Harvester"
    session_id = -1
    #allowed_domains = ["www.nasdaq.com"]
    start_urls = (
        'http://www.nasdaq.com/',
    )
    rules = ( Rule (
                LinkExtractor(allow=("", ), ),
                callback="parse_items", 
                follow=True
                ),
    )
    
    def __init__(self, session_id=-1, *args, **kwargs):
        super(HarvesterSpider, self).__init__(*args, **kwargs)
        self.session_id = session_id

    def parse(self, response):
        pass

    def parse_items(self, response):
        items = []
        item = Farm1Item()
        item["session_id"] = self.session_id
        item["depth"] = response.meta["depth"]
        item["current_url"] = response.url
        referring_url = response.request.headers.get("Referer", None)
        item["referring_url"] = referring_url
        item["title"] = response.xpath("//title/text()").extract()
        items.append(item)
        return items
