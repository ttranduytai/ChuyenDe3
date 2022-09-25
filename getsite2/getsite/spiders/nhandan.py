import scrapy
from getsite.items import GetsiteItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class NhandanSpider(scrapy.Spider):
    name = 'nhandan'
    allowed_domains = ['nhandan.vn']
    start_urls = ['https://nhandan.vn/']

    def parse(self, response):
        for link in response.css('.story__heading a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_posts)

    def parse_posts(self, response):
        nhandan_item = GetsiteItem()
        posts = response.css('.main-content.article')
        for post in posts:
                nhandan_item['title'] = post.css('.article__title.cms-title::text').get(),
                nhandan_item['date'] = post.css('.article__meta .time::text').get(),
                nhandan_item['content'] = post.css('.article__body.cms-body p::text').getall(),
                nhandan_item['category'] = post.css('.breadcrumbs .text::text').get(),
                nhandan_item['url'] = response.request.url,
        yield nhandan_item