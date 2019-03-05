import scrapy


class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['http://127.0.0.1:50422']
    custom_settings = dict(
        EXTENSIONS={
            'httplogging.HttpLogging': 100,
            'scrapy.extensions.closespider.CloseSpider': 200,
        },
        CLOSESPIDER_ERRORCOUNT=1,
    )

    def parse(self, response):
        pass
