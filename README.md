# wildberries

Присутствуют middlewares для Cookie и Proxy
Алгоритм запуска:

scrapy crawl proxy -O proxies.json # Чтобы получить список проксей
scrapy crawl wild -O wild.json # Запускаем парсер

Cookies в Response подтверждает регион Москва

С Proxies заметка:
  При заходе на глубину между 30-40 попыткой подключиться через Proxy
  Дефолтные Middlewares выбрасывают исключения прерывающие работу 
 
