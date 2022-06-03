import scrapy

class MeatScrape(scrapy.Spider):
    name = "meatprice"

    def start_requests(self):
        urls = [
            "https://www.wholesalemeatsdirect.co.nz/product-category/beef/",
            "https://www.wholesalemeatsdirect.co.nz/product-category/poultry/",
            "https://www.wholesalemeatsdirect.co.nz/product-category/lamb/",
            "https://www.wholesalemeatsdirect.co.nz/product-category/pork/",
            "https://www.wholesalemeatsdirect.co.nz/product-category/seafood/",
            "https://www.wholesalemeatsdirect.co.nz/product-category/value-packs/",
            "https://www.wholesalemeatsdirect.co.nz/product-category/specials/"
                ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,  response):
        even = 0
        try:
            for products in response.css("li.product"):
                yield {
                    "name": products.css("h2.woocommerce-loop-product__title::text").get(),
                    "price1": products.css("span.price bdi::text").get(),
                    "price2": products.css("span.price::text")[2].getall(),
                    "link": products.css("a").attrib["href"],
                }
                even += 2
        except IndexError:
            print("End of the range!")
    
        next_page = response.css("a.next.page-numbers").attrib["href"]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
