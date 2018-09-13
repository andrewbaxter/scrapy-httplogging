import logging
import pprint
# import inspect

from scrapy import signals
from scrapy.utils.gz import gunzip, gzip_magic_number


class HttpLogging(object):

    def __init__(self, crawler):
        self.logger = logging.getLogger('httplogging')
        crawler.signals.connect(
            self.log,
            signal=signals.response_downloaded)

    @classmethod
    def from_crawler(cls, crawler):
        return HttpLogging(crawler)

    def log(self, response, request, spider):
        body = response.body
        if gzip_magic_number(response):
            body = gunzip(body)
        self.logger.debug(
            # 'RESPONSE RECEIVED (callback {} {}:{})\n'
            'RESPONSE RECEIVED\n'
            'REQUEST {} {}\n{}\n{}\n\n'
            'RESPONSE {}\n{}\n{}...\n'.format(
                # request.callback.__name__,
                # inspect.getfile(request.callback),
                # inspect.getsourcelines(request.callback)[1],
                request.method,
                request.url,
                pprint.pformat(request.headers),
                request.body,
                response.status,
                pprint.pformat(response.headers),
                body[:1024],
            )
        )
