import json

import scrapy
from scrapy.exceptions import CloseSpider


class AdidasSpider(scrapy.Spider):
    name = "adidas"
    allowed_domains = ["www.adidas.ch"]
    start_urls = [
        f"https://www.adidas.ch/en/football-clothing?start={page_num}"
        for page_num in range(0, 1441, 48)
    ]

    def parse(self, response):
        all_ids = response.css("div[data-grid-id]::attr(data-grid-id)").getall()

        for id_item in all_ids:
            yield scrapy.Request(
                url=f"https://www.adidas.ch/api/search/product/{id_item}",
                callback=self.parse_second_level,
            )

    def parse_second_level(self, response):
        json_data = response.json()
        # json.dump(json_data, open("t.json", "w+"))

        yield {
            "url": self.allowed_domains[0] + json_data["link"],
            "title": json_data["name"],
            "data": "ADIDAS",
            "price": json_data["price"],
            "image": json_data["image"]["src"],
        }
