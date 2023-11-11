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
    start_urls = [start_urls[1]]
    print("#" * 100)
    print(start_urls)
    print("#" * 100)
    # exit()

    def parse(self, response):
        # Get all links to scrape here
        griditems = response.css('[role="listitem"]')
        for griditem in griditems:
            item_name = griditem.css("span.vh::text").get()
            item_url = griditem.css("div div div a::attr(href)").get()
            item_brand = griditem.css("strong::text").get()
            item_price = "".join(griditem.css("span.vtmn-price::text").getall()).strip()
            item_rating = griditem.css(
                "span.vtmn-rating_comment--secondary::text"
            ).get()

            print()
            print("*" * 100)
            print(item_name)
            print(item_url)
            print(item_brand)
            print(item_price)
            print(item_rating)
            print("*" * 100)
