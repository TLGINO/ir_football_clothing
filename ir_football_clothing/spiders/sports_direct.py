import scrapy
from currency_converter import CurrencyConverter


class SportsDirectSpider(scrapy.Spider):
    name = "sports_direct"
    allowed_domains = ["ch.sportsdirect.com"]
    start_urls = [
        f"https://ch.sportsdirect.com/football-shirts#dcp={i}&dppp=60&OrderBy=rank"
        for i in range(1, 18)
    ]
    currency_converter = CurrencyConverter()

    def parse(self, response):
        items = response.css("ul#navlist li")
        for item in items:
            item_url = item.css("::attr(li-url)").get()
            item_name = item.css("::attr(li-name)").get()
            item_brand = item.css("::attr(li-brand)").get().upper()
            item_price = round(
                self.currency_converter.convert(
                    float(item.css("::attr(li-price)").get().split(" ")[0]),
                    "EUR",
                    "CHF",
                ),
                2,
            )
            item_image = item.css("img::attr(src)").get()
            yield {
                "url": self.allowed_domains[0] + item_url,
                "title": item_name,
                "data": item_brand,
                "price": item_price,
                "image": item_image,
            }
