import json

import scrapy
from currency_converter import CurrencyConverter
from scrapy.selector import Selector


class DecathlonSpider(scrapy.Spider):
    name = "decathlon"
    allowed_domains = ["www.decathlon.co.uk"]
    start_urls = [
        f"https://www.decathlon.co.uk/sports/football/football-clothing?from={start}&size=40"
        for start in range(0, 961, 40)
    ]
    currency_converter = CurrencyConverter()

    def parse(self, response):
        # Get all links to scrape here
        griditems = response.css('[role="listitem"]')
        for griditem in griditems:
            item_url = griditem.css("div div div a::attr(href)").get()
            item_name = griditem.css("span.vh::text").get()
            item_brand = griditem.css("strong::text").get().upper()
            item_price = round(
                self.currency_converter.convert(
                    float(
                        "".join(griditem.css("span.vtmn-price::text").getall())
                        .strip()
                        .split("\n")[0][1:]
                    ),
                    "GBP",
                    "CHF",
                ),
                2,
            )
            item_image = griditem.css("img.svelte-11itto::attr(src)").get()

            yield {
                "url": self.allowed_domains[0] + item_url,
                "title": item_name,
                "data": item_brand,
                "price": item_price,
                "image": item_image,
            }
