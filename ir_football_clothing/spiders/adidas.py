import json

import scrapy
from scrapy.exceptions import CloseSpider


# This is useful
# https://docs.scrapy.org/en/latest/intro/tutorial.html
class AdidasSpider(scrapy.Spider):
    name = "adidas"
    allowed_domains = ["www.adidas.ch"]
    start_urls = [
        f"https://www.adidas.ch/en/football-clothing?start={page_num}"
        for page_num in range(0, 1441, 48)
    ]

    # scrapy shell https://www.adidas.ch/en/football-clothing?start=0
    def parse(self, response):
        all_ids = response.css("div[data-grid-id]::attr(data-grid-id)").getall()

        for id_item in all_ids:
            yield scrapy.Request(
                url=f"https://www.adidas.ch/api/search/product/{id_item}",
                callback=self.parse_second_level,
                meta={"id_item": id_item},
            )

    def parse_second_level(self, response):
        id_item = response.meta.get("id_item")

        with open("adidas_content_example.json", "w+") as f:
            json.dump(response.json(), f)
