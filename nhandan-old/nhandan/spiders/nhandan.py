import scrapy


class QuotesSpider(scrapy.Spider):
    name = "nhandan"

    def start_requests(self):
        urls = [
            'https://nhandan.vn/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'nhandan.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        title = response.xpath("//h2[@class='story__heading']/a[@class='cms-link']/text()").get()
        content = response.xpath("//time[@class='story__time']/text()").get()
        date = response.xpath("//div[@class='story__summary']/text()").get()
        print(title+"\n"+content+"\n"+date)