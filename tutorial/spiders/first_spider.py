import datetime, time
import json
<<<<<<< HEAD
import re 

import requests
import scrapy
import re

=======
import re

import requests
import scrapy

>>>>>>> 186de1a00fcdaf429fb6cb4caef21b0769ca2c1c

class ProxySpider(scrapy.Spider):
    name = 'proxy'
    start_urls = ['https://free-proxy-list.net/']

    def parse(self, response):
        for row in response.xpath("//tr"):
            # Получаем значения наличия https 
            isSecurity = row.xpath("td[@class='hx']/text()").get()
            if isSecurity == 'yes':
                ip, port = row.xpath('td/text()').getall()[:2]
                proxies = {
                    'http':'{}:{}'.format(ip, port),
                    'https': '{}:{}'.format(ip, port),
                }
                try:
                    # В случае неудача рейзит exception 
                    requests.get('https://www.wildberries.ru/', proxies=proxies, timeout=1)
                except: 
                    continue
                else: # Только в случае получения ответа записываем прокси в файл
                    yield {
                        'ip':ip,
                        'port':port,
                    }


class Wildberries(scrapy.Spider):
    name = 'wild'

    cookies = { # Только при отправке 5 кук получаю корректный куки в ответ
        '__cpns':'3_12_15_18',
        '__pricemargin':'1.0--',
        '__region':'75_68_69_63_33_40_48_70_64_1_4_30_71_22_38_31_66',
        '__store':'119261_117673_115577_507_3158_120602_6158_117501_120762_116433_119400_2737_117986_1699_1733_117413_119070_118106_119781',
        '__wbl':r'cityId%3D77%26regionId%3D77%26city%3D%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%26phone%3D84957755505%26latitude%3D55%2C7247%26longitude%3D37%2C7882'
    }

    def start_requests(self):
        # Оставил закоменченные юрлы, на которых тестировал скрапинг видео и view360
        urls = [
            # "https://www.wildberries.ru/catalog/10765528/detail.aspx", # Тут есть 360
            # "https://www.wildberries.ru/catalog/13248914/detail.aspx", # Еще 360
            # "https://www.wildberries.ru/catalog/3908404/detail.aspx", # Видео
            # "https://www.wildberries.ru/catalog/16182548/detail.aspx", # Ноутбуки показывают путю
            "https://www.wildberries.ru/catalog/yuvelirnye-izdeliya/zazhimy-i-zaponki",
        ]
        # С кукками все красиво
        for url in urls:
            yield scrapy.Request(url, callback=self.parse, cookies=self.cookies)
        
    def parse(self, response):
        """Помимо вытаскивания ссылок и перехода по страницам магазина
        В данном методе так же сразу вытаскивается section, который передается
<<<<<<< HEAD
        в последующие функции, т.к. на страницах товаров редко присутствует дерево секций 
        """
        attr = [] # Тут будет хранится секция 
=======
        в последующие функции, т.к. на страницах товаров редко присутствует дерево секций.
        """
        attr = [] 
>>>>>>> 186de1a00fcdaf429fb6cb4caef21b0769ca2c1c
        for i in response.xpath('//script').getall():
            r = re.findall(r'google_tag_params', i)
            if len(r) > 0:
                # TODO собрать в одну регулярку 
                s = i.replace('\n', '')
                b = re.findall('"Pcat": (.*)]', s)
                attr = re.findall('"(.*)"', b[0])  # Нужный массив
        # Вместе с запросом передаем dict(meta) для получения секций в итоговом объекте
        for element in response.css('div.j-card-item'):
            product_url = element.css('a.j-open-full-product-card::attr(href)').get().split('?')[0]
            product_url = response.urljoin(product_url)
            yield scrapy.Request(product_url, callback=self.schedule_data, cookies=self.cookies, meta={'section':attr})
        # Возможно, необходимо переписать follow на Request. Но это тема для обсуждения, поэтому пока что оставлю 
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)

    def schedule_data(self, response):
        """Решил вынести логику длинее одной строки в отдельный метод,
        после того, как его размеры увеличились. 
<<<<<<< HEAD
        Код стало гораздо удобнее читать и исправлять 
=======
        Код стало гораздо удобнее читать и исправлять.
>>>>>>> 186de1a00fcdaf429fb6cb4caef21b0769ca2c1c
        """
        data_view = {}
        data_view['timestamp'] = self.extract_data(response, key='timestamp')
        data_view['RPC'] = self.extract_data(response, key='RPC')
        data_view['url'] = response.url
        data_view['marketing_tags'] = response.css('li.tags-group-item.j-tag a::text').getall()
        data_view['title'] = self.extract_data(response, key='title')
        data_view['brand'] = response.css('span.brand::text').get()
        data_view['section'] = response.meta['section']
        data_view['price_data'] = self.extract_data(response, key='price_data')
        data_view['stock'] = self.extract_data(response, key='stock')
        data_view['metadata'] = self.extract_data(response, key='metadata')
        data_view['assets'] = self.extract_data(response, key='assets')
        data_view['variants'] = self.extract_data(response, key='variants')

        yield data_view

    def extract_data(self, response, key):
<<<<<<< HEAD
        """Метод получает ключ и возвращает результат
        выполнения функции вычисления значения ключа 
=======
        """ Метод получает ключ и возвращает результат
        выполнения функции вычисления значения ключа.
>>>>>>> 186de1a00fcdaf429fb6cb4caef21b0769ca2c1c
        """
        def get_timestamp(response):
            """Возвращает время timestamp"""
            # Unix timestamp. ex. 1608985712
            unix = time.mktime(datetime.datetime.now().timetuple())
            result = str(int(unix))
            # Date time format. ex 26.12.2020 16:48
            # value = datetime.datetime.fromtimestamp(unix)
            # result =  value.strftime('%d.%m.%Y %H:%M')
            return result

        def get_RPC(response):
<<<<<<< HEAD
            """RPC поулчаем из URL товара. Так же он
            совпадает с Артиклем товара 
=======
            """ RPC поулчаем из URL товара. Так же он
            совпадает с Артиклем товара.
>>>>>>> 186de1a00fcdaf429fb6cb4caef21b0769ca2c1c
            """
            return str(response.url.split('/')[-2])
        
        def get_title(response):
            """Получаем имя товара и цвет при наличии """
            name = response.css('span.name::text').get()
            color = response.css('span.color::text').get()
            if color is not None:
                return '{}, {}'.format(name, color)
            return name

        def get_price(response):
            """Вычисляем цену. Если есть скидка берем значения старой и новой цены
            после чего вычисляем процент скидки на позицию 
            """
            try:
                final_cost = response.css('span.final-cost::text').get()
                current = float(''.join(list(filter(lambda x: x.isdigit(), final_cost))))
                old_price = response.css('span.old-price').get()
                if old_price is not None: 
                    # Если есть старая цена нужно вычислить скидку
                    origin = float(''.join(list(filter(lambda x: x.isdigit(), old_price))))
                    sale_tag = int(100 - ((100*current)/origin))
                    return {
                        'current': current,
                        'origin': origin,
                        'sale_tag': 'Скидка {}%'.format(sale_tag),
                    }
            # Если товар отсутствует будет брошено исключение
            except TypeError:
                current = float(0)
            # Если скидки нет - возвращаем следующий словарь
            return {
                'current': current,
                'origin': current,
            }

        def get_stock(response):
            """Получаем значения наличия товара. Данные о кол-ве оставшихся
            до сих пор не нашел. Текущий код не долговечен, т.к. json хранящий информацию
            находтися под комментарием:" Удалить, когда гугл что-то там поменяет" 
            """
            in_stock = ""
            for item in response.xpath('//script'): 
                r = re.findall(r'data: {.*', item.get()) # Получаем словарь data
                if len(r) > 0:
                    in_stock = re.findall(r'"isSoldOut":(\w+)', r[0])[0] # Получаем значения ключа isSoldOut
                    break
            return {
                'in_stock': True if in_stock == 'false' else False,
                'count': 0,
            }

        def get_assets(response):
            """Это было интересно. Сразу берем главную картинку и список
            всех остальных. Дальше проверяем наличие видео и view360, в случае 
<<<<<<< HEAD
            наличия - вычисляем и их. Аккуратно! Ниже хрупкий костыль 
=======
            наличия - вычисляем и их. Аккуратно! Ниже хрупкий костыль
>>>>>>> 186de1a00fcdaf429fb6cb4caef21b0769ca2c1c
            """
            add_prefix = lambda x: 'https:' + str(x)
            result = {            
                'main_image': add_prefix(response.css('a.j-photo-link::attr(href)').get()), # Ссылка на основное изображение товара
                'set_image':  list(map(add_prefix, response.css('a.j-photo-link::attr(href)').getall())), # Список всех изображений товара
                'video': [],
                'view360': [],
            }
            # В первую очередь проверяем наличие 360 и Видео на товаре
            has_video, has_view360 = "", ""
            for item in response.xpath('//script'):
                r = re.findall(r'data: {.*', item.get()) # Получаем словарь data
                if len(r) > 0:
                    has_video = re.findall(r'"hasVideo":(\w+)', r[0])[0]
                    has_view360 = re.findall(r'"has3D":(\w+)', r[0])[0]
            # Если есть видео добавляем
            if has_video == 'true': 
                for selector in response.xpath("//meta[@property='og:video']").getall():
                    result['video'] = list(map(add_prefix, re.findall(r'content="(.*)"', selector)))

            # А тут костыльное решение сильно замедляющее работу
            if has_view360 == 'true':
                root = 'https:' + response.css("div#container_3d::attr(data-path)").get()
                counter = 0
                while True: # Какую прекрасную багулину тут словил, когда mapper сразу вычислял функции
                    if requests.get('{}/{}.jpg'.format(root, counter)).status_code == 404:
                        break
                    result['view360'].append('{}/{}.jpg'.format(root, counter))
                    counter += 1

            return result

        def get_meta(response):
<<<<<<< HEAD
            """Возвращает словарь содержащий описание, а так же 
            все параметры, находящиеся на странице позиции 
=======
            """ Возвращает словарь содержащий описание, а так же 
            все параметры, находящиеся на странице позиции
>>>>>>> 186de1a00fcdaf429fb6cb4caef21b0769ca2c1c
            """
            result = {'__description':  response.css('div.j-description p::text').get()} # Описание есть у всех товаров
            for param in response.css('div.pp'): # А дальше проходим по списку параметров
                result[param.css('b::text').get()] = param.css('span::text').get()
            return result

        def get_variants(response):
            """Получаем кол-во вариантов товаров. Хранятся в блоке options """
            variants = len(response.css('div.options div div ul li').getall())
            return 1 if variants == 0 else variants # Если options.li пуст - значит всего 1 вариант

        # Mapper соотносит ключ с функцией 
        mapper = {
            'timestamp': get_timestamp,
            'RPC': get_RPC,
            'title': get_title,
            'price_data': get_price,
            'stock': get_stock,
            'metadata': get_meta,
            'assets': get_assets,
            'variants': get_variants,
        }

        return mapper[key](response)