from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "wion"
    start_urls = [
        'https://www.wionews.com/india-news',

    ]

    def parse(self, response):
        for newsItem in response.css('div.article-list-txt'):
            href = newsItem.css('h2 a::attr(href)').get()
            # contentPage = scrapy.Request(
            #     href, callback=self.parse_inside, cb_kwargs=dict())
            # contentPage.cb_kwargs['heading'] = newsItem.css(
            #     'h2 a::text').get()
            # contentPage.cb_kwargs['author'] = newsItem.css(
            #     'p.by-author a::text').get()
            # contentPage.cb_kwargs['publish_date'] = newsItem.css(
            #     'div.date-author-loc li::text')
            # contentPage.cb_kwargs['overview'] = newsItem.css(
            #     'p::text').get()
            # contentPage.cb_kwargs['link'] = newsItem.css(
            #     'h2 a::attr(href)').get()
            yield {
                'heading': newsItem.css(
                    'h2 a::text').get(),
                'author': newsItem.css(
                    'p.by-author a::text').get(),
                'publish_date': newsItem.css(
                    'p::text').get(),
                'overview': newsItem.css(
                    'p::text').get(),
                'link': newsItem.css(
                    'h2 a::attr(href)').get(),
                # 'content': response.css('div.article-main-data p::text').getall()
            }
            # yield contentPage
            # nextPage = response.css(
            #     'div.listng_pagntn span + a::attr(href)').get()
            # if nextPage is not None:
            #     yield scrapy.Request(nextPage, callback=self.parse)

    def parse_inside(self, response, heading, author, publish_date, overview, link):
        yield {
            'heading': heading,
            'author': author,
            'publish_date': publish_date,
            'overview': overview,
            'link': link,
            'content': response.css('div.article-main-data p::text').getall()
        }
