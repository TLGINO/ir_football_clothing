import json

import scrapy
from scrapy.selector import Selector


class DecathlonSpider(scrapy.Spider):
    name = "decathlon"
    allowed_domains = ["www.decathlon.co.uk"]
    start_urls = [
        f"https://www.decathlon.co.uk/sports/football/football-clothing?from={start}&size=40"
        for start in range(0, 961, 40)
    ]

    def parse(self, response):
        # Get all links to scrape here
        griditems = response.css('[role="listitem"]')
        for griditem in griditems:
            item_url = griditem.css("div div div a::attr(href)").get()
            item_name = griditem.css("span.vh::text").get()
            item_brand = griditem.css("strong::text").get()
            item_price = "".join(griditem.css("span.vtmn-price::text").getall()).strip()
            item_image = griditem.css("img.svelte-11itto::attr(src)").get()

            yield {
                "url": self.allowed_domains[0] + item_url,
                "title": item_name,
                "data": item_brand,
                "price": item_price,
                "image": item_image,
            }
