import scrapy


class SportsDirectSpider(scrapy.Spider):
    name = "sports_direct"
    allowed_domains = ["ch.sportsdirect.com"]
    start_urls = [f"https://ch.sportsdirect.com/football-shirts#dcp={i}&dppp=60&OrderBy=rank" for i in range(1, 18)]

    def parse(self, response):


        
        items = response.css("ul#navlist li")
        for item in items:
            item_url = item.css("::attr(li-url)").get()
            item_name = item.css("::attr(li-name)").get()
            item_brand = item.css("::attr(li-brand)").get()
            item_price = item.css("::attr(li-price)").get() + " EUR"
            item_image = item.css("img::attr(src)").get()
            yield {
                "url": self.allowed_domains[0] + item_url,
                "title": item_name,
                "data": item_brand,
                "price": item_price,
                "image": item_image,
            }
