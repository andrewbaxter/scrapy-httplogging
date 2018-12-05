from __future__ import unicode_literals
from scrapy import signals
from scrapy.utils.gz import gunzip
from scrapy.utils.project import get_project_settings

import logging
import pprint


class HttpLogging(object):
    def __init__(self, crawler):
        self.logger = logging.getLogger('httplogging')
        self.nocolors = get_project_settings().get('HTTPLOGGING_NOCOLORS', False)
        crawler.signals.connect(self.log, signal=signals.response_downloaded)

    @classmethod
    def from_crawler(cls, crawler):
        return HttpLogging(crawler)

    def log(self, response, request, spider):
        try:
            body = gunzip(response.body)
        except IOError:
            body = response.body

        pp = pprint.PrettyPrinter(indent=2)

        msg_template = self._get_template()
        data = [
            request.method,
            request.url,
            pp.pformat(request.headers),
            pp.pformat(request.body),
            response.status,
            pp.pformat(response.headers),
            pp.pformat(body[:1024]),
        ]
        self.logger.debug(msg_template.format(*data))

    def _get_template(self):
        if self.nocolors:
            return (
                'RESPONSE RECEIVED\n'
                'REQUEST {} {}\n{}\n{}\n{}\n\n'
                'RESPONSE {}\n{}\n{}...\n'
            )
        else:
            h1 = '\033[1m\033[93m'
            h2 = '\033[1m'
            h3 = '\033[4m'
            end = '\033[0m'
            under = '\033[4m'
            line1_begin = '\033[32m\u250f' + (78 * '\u2501') + '\u2513' + end
            line1_end = '\033[32m\u2517' + (78 * '\u2501') + '\u251b' + end
            line2 = '\033[32m' + (76 * '\u2500') + end
            line3 = '\033[32m' + (76 * '\u2504') + end

            return '\n'.join(
                [
                    '',
                    '{line1_begin}',
                    '  {h1}RESPONSE RECEIVED{end}',
                    '  {line2}',
                    '  {h2}REQUEST {{}} {under}{{}}{end}',
                    '  {line3}',
                    '  {h3}Headers{end}:',
                    '  {{}}',
                    '  {h3}Body{end}:',
                    '  {{}}',
                    '  {line2}',
                    '  {h2}RESPONSE {{}}{end}',
                    '  {line3}',
                    '  {h3}Headers{end}:',
                    '  {{}}',
                    '  {h3}Body{end}:',
                    '  {{}}...',
                    '{line1_end}',
                ]
            ).format(
                end=end,
                h1=h1,
                h2=h2,
                h3=h3,
                line1_begin=line1_begin,
                line1_end=line1_end,
                line2=line2,
                line3=line3,
                under=under,
            )
