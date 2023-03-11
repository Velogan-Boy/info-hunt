from pathlib import Path

import scrapy


class NdtvSpider(scrapy.Spider):
    name = "ndtv"
    start_urls = [
        'https://www.ndtv.com/education',
        'https://www.ndtv.com/india',
        'https://www.ndtv.com/world-news',
        'https://www.ndtv.com/science',
        'https://www.ndtv.com/latest'
    ]

    def parse(self, response):
        for newsItem in response.css('div.news_Itm'):
            href = newsItem.css('h2.newsHdng a::attr(href)').get()
            yield from self.downloader(response, newsItem, href)

    def downloader(self, response, newsItem, href):
            contentPage = response.follow(
                href, callback=self.parse_inside, cb_kwargs=dict())
            contentPage.cb_kwargs['heading'] = newsItem.css(
                'h2.newsHdng a::text').get()
            contentPage.cb_kwargs['author'] = newsItem.css(
                'span.posted-by a::text').get()
            contentPage.cb_kwargs['publish_date'] = newsItem.css(
                'span.posted-by').re('\| (\w+) (\w+) (\w+), (\w+)')
            contentPage.cb_kwargs['overview'] = newsItem.css(
                'p.newsCont::text').get()
            contentPage.cb_kwargs['link'] = newsItem.css(
                'h2.newsHdng a::attr(href)').get()
            yield contentPage
            yield from self.navigator(response)

    def navigator(self, response):
            nextPage = response.css(
                'div.listng_pagntn span + a::attr(href)').get()
            if nextPage is not None:
                yield response.follow(nextPage, callback=self.parse)

    def parse_inside(self, response, heading, author, publish_date, overview, link):
        yield {
            'heading': heading,
            'author': author,
            'publish_date': publish_date,
            'overview': overview,
            'link': link,
            'content': response.css('div.ins_storybody > p::text').getall()
        }
