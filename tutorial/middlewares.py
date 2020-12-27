# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from random import randint
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ProxyMiddleware:
    """ Берем прокси лист, выбираем рандомную прокси 
    и пытаемся подключиться - в случае неудаи выкидываем из списка 
    """

    def __init__(self, proxy_list, proxy_tries, proxy_timeout):
        self.proxy_list = proxy_list
        self.timeout = proxy_timeout
        self.tries = proxy_tries

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = crawler.settings
        fields = crawler.settings.get('PROXY_SETTINGS', False)
        # Initial 
        mw = cls(
            proxy_list = fields['PROXY_LIST'],
            proxy_tries = fields['PROXY_RETRY_COUNT'],
            proxy_timeout = fields['PROXY_TIMEOUT'],
        )

        crawler.signals.connect(mw.spider_opened, signal=signals.spider_opened)

        return mw

    def process_request(self, request, spider):
        """ Метод выбирает случайную проксю из списка. 
        Если список прокси пуст - выбирает стандартный хост """
        # Проверка существования прокси и назначения в случае наличияя
        if len(self.proxy_list) > 0:
            proxy = self.proxy_list[randint(0, len(self.proxy_list)-1)]
            proxy = self.proxy_list[0]
            request.meta['proxy'] = proxy
            spider.logger.info('[PROXY]: Proxy choosen {}'.\
                format(proxy))
        # Оповещяем пользователя об использования стандратного хоста
        else:
            spider.logger.info('[PROXY]: Standart host')
        # Без таймаута не дождемся ничего
        request.meta['download_timeout'] = self.timeout
        request.meta['max_retry_times'] = self.tries
        return None

    def process_exception(self, request, exception, spider):
        """ В случае 3х неудачных попыток выкидываем проки из списка """
        if len(self.proxy_list) > 0:
            self.proxy_list.remove(request.meta['proxy'])
            spider.logger.info(
                '[PROXY]: Proxy {} was dropped. {} Proxies left'.\
                    format(request.meta['proxy'], len(self.proxy_list)))
            # Если прокси закончились оповестим пользователя
            if len(self.proxy_list) == 0:
                spider.logger.info(
                    '[PROXY]: Proxies are over. Using standart host')
            request.meta['proxy'] = None
            request.meta['retry_times'] = 0
            return request
        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
