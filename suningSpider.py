# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy

class SuningspiderSpider(scrapy.Spider):
    name = 'suningSpider'
    allowed_domains = ['suning.com']
    start_urls = ['https://www.suning.com/pinpai/1804-502282-0.html']

    def parse(self, response):
        cate_text = response.xpath('//div[@class="clearfix"]/a/@title')
        cate_href = response.xpath('//div[@class="clearfix"]/a/@href')
        for i, j in zip(cate_text, cate_href):
            item = {}
            item["b_cate"] = i
            item['cate_url'] = 'https://www.suning.com' + j
            yield scrapy.Request(item['cate_url'], callback=self.parse_book, meta={"item": item})

    def parse_book(self, response):
        item = deepcopy(response.meta["item"])
        # 图书列表页分组
        li_list = response.xpath("//div[@class='filtrate-books list-filtrate-books']/ul/li")
        for li in li_list:
            item["book_name"] = li.xpath(".//div[@class='book-title']/a/@title").extract_first()
            item["book_img"] = li.xpath(".//div[@class='book-img']//img/@src").extract_first()
            if item["book_img"] is None:
                item["book_img"] = li.xpath(".//div[@class='book-img']//img/@src2").extract_first()
            item["book_author"] = li.xpath(".//div[@class='book-author']/a/text()").extract_first()
            item["book_press"] = li.xpath(".//div[@class='book-publish']/a/text()").extract_first()
            item["book_desc"] = li.xpath(".//div[@class='book-descrip c6']/text()").extract_first()
            item["book_href"] = li.xpath(".//div[@class='book-title']/a/@href").extract_first()
            yield scrapy.Request(
                item["book_href"],
                callback=self.parse_book_detail,
                meta={"item": deepcopy(item)}
            )

        # 翻页
        page_count = int(re.findall("var pagecount=(.*?);", response.body.decode())[0])
        current_page = int(re.findall("var currentPage=(.*?);", response.body.decode())[0])
        if current_page < page_count:
            next_url = item["s_href"] + "?pageNumber={}&sort=0".format(current_page + 1)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book,
                meta={"item": response.meta["item"]}
            )

    def parse_book_detail(self, response):
        item = response.meta["item"]
        item["book_price"] = re.findall("\"bp\":'(.*?)',", response.body.decode())
        item["book_price"] = item["book_price"][0] if len(item["book_price"]) > 0 else None
        print(item)

