import scrapy


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
        category = response.css("h1.page-title::text").get(default="").strip()

        for product in products:

            yield {
                "category": category,
                "title": product.css("h2.product-name a::text").get(),
                "url": product.css("h2.product-name a::attr(href)").get(),
                "price": product.css(
                "div.price-wrap span.price span.woocommerce-Price-amount bdi::text"
            ).get()
            }

        next_page = response.css("div.infload-controls a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category)
