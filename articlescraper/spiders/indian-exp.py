from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "indian-express"
    start_urls = [
        'https://indianexpress.com/section/india/'
    ]

    def parse(self, response):
        for newsItem in response.css('div.articles'):
            href = newsItem.css('h2 a::attr(href)').get()
            contentPage = scrapy.Request(
                href, callback=self.parse_inside, cb_kwargs=dict())
            contentPage.cb_kwargs['heading'] = newsItem.css(
                'h2.title a::text').get()
            contentPage.cb_kwargs['author'] = ""
            contentPage.cb_kwargs['publish_date'] = newsItem.css(
                'div.date::text').get()
            contentPage.cb_kwargs['overview'] = newsItem.css(
                'p::text').get()
            contentPage.cb_kwargs['link'] = newsItem.css(
                'h2.title a::attr(href)').get()
            yield contentPage
            nextPage = response.css(
                'ul.page-numbers span + a::attr(href)').get()
            if nextPage is not None:
                yield scrapy.Request(nextPage, callback=self.parse)

    def parse_inside(self, response, heading, author, publish_date, overview, link):
        yield {
            'heading': heading,
            'author': author,
            'publish_date': publish_date,
            'overview': overview,
            'link': link,
            'content': response.css('div.full-details p::text').getall()
        }
