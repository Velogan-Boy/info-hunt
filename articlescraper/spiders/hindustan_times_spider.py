from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "hindustan-times"
    start_urls = [
        'https://www.hindustantimes.com/cricket'
    ]

    def parse(self, response):
        for newsItem in response.css('div.cartHolder'):
            href = newsItem.css('h3 a::attr(href)').get()
            contentPage = scrapy.Request(
                href, callback=self.parse_inside, cb_kwargs=dict())
            contentPage.cb_kwargs['heading'] = newsItem.css(
                'h3.hdg3 a::text').get()
            contentPage.cb_kwargs['author'] = newsItem.css(
                'small.byLineAuthor a::text').get()
            contentPage.cb_kwargs['publish_date'] = ""
            contentPage.cb_kwargs['overview'] = newsItem.css(
                'h2.sortDec::text').get()
            contentPage.cb_kwargs['link'] = newsItem.css(
                'h3.hdg3 a::attr(href)').get()
            yield contentPage
        nextPage = response.css(
            'li.next a::attr(href)').get()
        if nextPage is not None:
            yield scrapy.Request(nextPage, callback=self.parse)

    def parse_inside(self, response, heading, author, publish_date, overview, link):
        yield {
            'heading': heading,
            'author': author,
            'publish_date': publish_date,
            'overview': overview,
            'link': link,
            'content': response.css('div.detail  p::text').getall()
        }
