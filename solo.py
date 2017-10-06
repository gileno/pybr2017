import scrapy


class PythonSpider(scrapy.Spider):

    name = 'python'

    def start_requests(self):
        yield scrapy.Request(
            url='http://www.python.org', callback=self.parse
        )

    def parse(self, response):
        self.log('URL acessada: {}'.format(response.url))
