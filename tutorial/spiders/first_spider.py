import datetime, time
import scrapy


data_view = {
    'timestamp': None, # timestamp
    'RPC': None, # UUID
    'url': None, # ссылка на страницу товара 
    'title': None, # Заголовок, название товара
    'marketing_tags': None, # Tags ['one', 'two', 'three']
    'brand': None, # Бренд Товара
    'section': None, # ['root','root's child']
    'price_data': {
        'current':None, # Цена со скидкой
        'original': None,
        'sale_tag': None, # Процент скидки
    },
    'stock':{
        'in_stock': None, # Bool(Наличие товара)
        'count': None, # Если есть информация о кол-ве товара, иначе 0
    },
    'assets':{
        'main_image': None, # Ссылка на основное изображение товара
        'set_image': None, # Список всех изображений товара
        'view360': None, # Видимо ссылкан на 360, если имеется
        'video': None, # Список видео
    },
    'metadata':{
        '__description':None, # Описание товара,
    },
    'variants':  None, # Integer varitans of the position
}


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    start_urls = ['https://free-proxy-list.net/']

    def parse(self, response):
        for row in response.xpath("//tr"):
            # Получаем значения наличия https 
            isSecurity = row.xpath("td[@class='hx']/text()").get()
            if isSecurity == 'yes':
                ip, port = row.xpath('td/text()').getall()[:2]
                yield {
                    'ip':ip,
                    'port':port,
                }

class Wildberries(scrapy.Spider):
    name = 'wild'

    def start_requests(self):
        url = 'https://www.wildberries.ru/catalog/yuvelirnye-izdeliya/zazhimy-i-zaponki'
        __wbl = r'cityId%3D4355%26regionId%3D34%26city%3D%D0%92%D0%BE%D0%BB%D0%B3%D0%BE%D0%B3%D1%80%D0%B0%D0%B4%26phone%3D88001007505%26latitude%3D48%2C707073%26longitude%3D44%2C51693'
        region = r'75_68_69_63_33_40_48_70_64_1_4_30_71_22_38_31_66'
        store = r'115577_116433_117501_507_3158_120602_6158_119400_120762_2737_117986_1699_1733_117673_119261_117413_119070_118106_119781'

        yield scrapy.Request(url, callback=self.parse
        , cookies={
                '__wbl':__wbl,
                '__region':region,
                '__store':store,
            })
        # yield scrapy.Request(url, callback=self.parse, meta={'proxy':'http://{}:{}'.format(proxy['ip'], proxy['port'])})

    def parse(self, response):
        for element in response.css('div.j-card-item'):
            product_url = element.css('a.j-open-full-product-card::attr(href)').get().split('?')[0]
            yield response.follow(product_url, callback=self.get_data)
        

        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def get_data(self, response):
        data_view = {}
        # timestamp ( если нужен все же читабельный вид, то
        data_view['timestamp'] = str(int(time.mktime(datetime.datetime.now().timetuple())))
        # RPC - Артикль и URL товара
        data_view['RPC'] = str(response.url.split('/')[-2])
        data_view['url'] = response.url
        # Почти все товары имеют цвет
        data_view['title'] = '{}, {}'.format(response.css('span.name::text').get(), response.css('span.color::text').get())
        data_view['brand'] = response.css('span.brand::text').get()
        # Секция была выбрана заранее
        data_view['section'] = ['Ювелирные изделия', 'Зажимы, запонки, ремни']
        # Ниже цены    
        current = ''.join(list(filter(lambda x: x.isdigit(), response.css('span.final-cost::text').get()))) # Строка содержит много хлама, нас интересуют только цифры
        data_view['price_data'] = {
            'current': current,
        }
        if response.css('div.c-text-base::text').get() is not None:
            origin = ''.join(list(filter(lambda x: x.isdigit(), response.css('div.c-text-base::text').get())))
            data_view['price_data']['origin'] = origin
            data_view['price_data']['sate_tag'] = "Скидка: {}%".format(get_delta(current, origin))
        # Нигде не увидел отображения наличия\отсутствия товаров. Везде самовывоз
        data_view['stock'] = {
            'in_stock': True,
            'count': 0,
        }
        # Помимо описания у всех товаров одинаковая структура параметров
        data_view['meta'] = {
            '__description':  response.css('div.j-description p::text').get()
        }
        for param in response.css('div.pp'):
            data_view['meta'][param.css('b::text').get()] = param.css('span::text').get()
        # Фоточки
        data_view['assets'] = {
            'main_image': response.css('a.j-photo-link::attr(href)').get(), # Ссылка на основное изображение товара
            'set_image': response.css('a.j-photo-link::attr(href)').getall(), # Список всех изображений товара
            'view360': [],
            'video': [], 
        }
        data_view['variants'] = 1

        yield data_view

    def get_delta(current, origin):
        return int(origin) - int(current)