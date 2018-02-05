# -*- coding: utf-8 -*-

import json

import scrapy
from scrapy.http.request import Request
from spider_project.items import SpiderProjectItem

from six.moves.urllib import parse

class Ajax_extractSpider(scrapy.Spider):
    taskid = "ajax_extract"
    name = taskid
    entry = "exercise/detail_ajax"

    def start_requests(self):
        prefix = self.settings["WEB_APP_PREFIX"]
        result = parse.urlparse(prefix)
        base_url = parse.urlunparse(
            (result.scheme, result.netloc, "", "", "", "")
        )
        url = parse.urljoin(base_url, self.entry)
        yield Request(
            url=url,
            callback=self.parse_entry_page
        )

    def parse_entry_page(self, response):
        # since we found out the real ajax url, so when dealing with entry url
        # we yield ajax request to get the real data
        result = parse.urlparse(response.url)
        base_url = parse.urlunparse(
            (result.scheme, result.netloc, "", "", "", "")
        )
        ajax_url = parse.urljoin(base_url, "exercise/ajaxdetail")
        yield Request(
            url=ajax_url,
            callback=self.parse_ajax_page
        )

    def parse_ajax_page(self, response):
        json_data = json.loads(response.body.decode("utf-8"))

        item = SpiderProjectItem()
        item["taskid"] = self.taskid
        data = {}
        data["title"] = json_data["title"]
        data["price"] = json_data["price"]
        item["data"] = data
        yield item

