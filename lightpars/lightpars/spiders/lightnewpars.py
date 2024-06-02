import scrapy


class LightnewparsSpider(scrapy.Spider):
    name = "lightnewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://divan.ru/category/svet"]

    def parse(self, response):
        categories = response.css('div.ui-j6Lq6 a::attr(href)').getall()
        for category_url in categories:
            yield response.follow(category_url, self.parse_category)

    def parse_category(self, response):
        products = response.css('div[data-testid="product-card"]')

        for product in products:
            product_url = product.css('a::attr(href)').get()
            product_name = product.css('span[itemprop="name"]::text').get()
            product_price = product.css('meta[itemprop="price"]::attr(content)').get()

            yield {
                'name': product_name,
                'price': product_price,
                'url': response.urljoin(product_url),
            }

