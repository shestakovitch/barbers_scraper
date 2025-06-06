import scrapy
from barbers_scraper.items import BarbersItem


class BarbersSpider(scrapy.Spider):
    name = "barbers"
    allowed_domains = ["barbers.rs"]
    start_urls = ["https://www.barbers.rs/"]

    def parse(self, response):
        # Ищем категории в мобильном меню
        category_links = response.css("div.js-slinky-menu a.menu__item::attr(href)").getall()
        for link in category_links:
            if "/kategorija/" in link:
                yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        products = response.css("li.product-item")
        barbers_item = BarbersItem()


        for product in products:

            barbers_item["category"] = response.css("h1.page-title::text").get(default="").strip()
            barbers_item["title"] = product.css("h2.product-name a::text").get()
            barbers_item["url"] = product.css("h2.product-name a::attr(href)").get()
            barbers_item["price"] = product.css(
                "div.price-wrap span.price span.woocommerce-Price-amount bdi::text"
            ).get()

            yield barbers_item

        next_page = response.css("div.infload-controls a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category)
