import logging

from scrapy import signals
from scrapy.exceptions import NotConfigured


class HttpLogging(object):

    def __init__(self, crawler):
        if not crawler.settings.getbool('HTTPLOGGING_ENABLED'):
            raise NotConfigured
        self.logger = logging.getLogger('httplogging')
        crawler.signals.connect(
            self.log,
            signal=signals.response_received)

    @classmethod
    def from_crawler(cls, crawler):
        return HttpLogging(crawler)

    def log(self, response, request, spider):
        request = response.request
        self.logger.debug(
            'RESPONSE RECEIVED\n'
            'REQUEST {} {}\n{}\n{}\n\n'
            'RESPONSE {}\n{}\n{}...\n'.format(
                request.method,
                request.url,
                request.headers,
                request.body,
                response.status,
                response.headers,
                response.body[:1024],
            )
        )
