# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from farm1.items import Farm1Item
from urlparse import urlparse

class Harvester2(CrawlSpider):
    name = "Harvester2"
    session_id = -1
    response_url = ""
    start_urls = (
        'http://www.mmorpg.com',
    )

    #rule preckudes any relative urls by only allowing urls that start with a URI Scheme
    rules = (
        Rule(
            LinkExtractor(allow=("((mailto\:|(news|(ht|f)tp(s?))\://){1}\s+)", ),),
            callback = "parse_items",
            process_links = "filter_link",
            follow = True
        ),
    )

    def __init__(self, session_id=-1, *args, **kwargs):
        super(Harvester2, self).__init__(*args, **kwargs)
        self.session_id = session_id

    #overrides the base definition and is called only for
    #the defined start_urls
    #initializes the response_url before any crawling
    def parse_start_url(self, response):
        self.response_url = response.url
        return self.parse_items(response)


    '''
    when a response is sent to spider for processing
    the filter_link() is called before process_item()
    '''
    def parse_items(self, response):
        self.response_url = response.url
        items = []
        item = Farm1Item()
        item["session_id"] = self.session_id
        item["depth"] = response.meta["depth"]
        item["title"] = response.xpath('//title/text()').extract()
        item["current_url"] = response.url
        referring_url = response.request.headers.get('Referer', None)
        item["referring_url"] = referring_url
        items.append(item)
        return items

    #links which contain the base domain are filtered out
    def filter_links(self, links):
        baseDomain = self.get_base_domain(self.response_url)
        filteredLinks = []
        for link in links:
            if link.url.find(baseDomain) < 0:
                filteredLinks.append(link)
        return filteredLinks

    #get base domain
    def get_base_domain(self, url):
        #netloc
        base = urlparse(url).netloc
        if base.upper().startswith("WWW."):
            base = base[4:]
        elif base.upper().startswith("FTP."):
            base = base[4:]
        #drop any ports
        base = base.split(":")[0]
        return base

