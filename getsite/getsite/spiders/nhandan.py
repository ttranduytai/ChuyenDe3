import scrapy


class NhandanSpider(scrapy.Spider):
    name = 'nhandan'
    allowed_domains = ['nhandan.vn']
    start_urls = ['http://nhandan.vn/']

    def parse(self, response):
        for link in response.css('.story__heading a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_categories)

    def parse_categories(self, response):
        products = response.css('.main-content.article')
        for product in products:
            yield {
                'title': product.css('.article__title.cms-title::text').get(),
                'date': product.css('.article__meta .time::text').get(),
                'content': product.css('.article__body.cms-body p::text').getall(),
            }