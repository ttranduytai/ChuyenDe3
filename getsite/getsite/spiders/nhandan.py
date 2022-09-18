import scrapy


class NhandanSpider(scrapy.Spider):
    name = 'nhandan'
    allowed_domains = ['nhandan.vn']
    start_urls = ['http://nhandan.vn/']

    def parse(self, response):
        for link in response.css('.story__heading a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_categories)

    def parse_categories(self, response):
        products = response.css('.story__heading')
        for product in products:
            yield {
                'name': product.css('.cms-link::text').get().strip(),
                'link': product.css('.cms-link::attr(href)').get().strip(),
            }