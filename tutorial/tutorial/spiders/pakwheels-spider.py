import json
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PakwheelsUsedCarsSpider(CrawlSpider):
    name = "pakwheels"
    ad_descriptions = []
    start_urls = [
        "https://www.pakwheels.com/used-cars/search/-/"
    ]

    rules = (
         Rule(LinkExtractor(allow=r"https://www.pakwheels.com/used-cars/search/-/\?page=\d+", restrict_css="li.next_page a"),  
              callback="parse", 
              follow=True
            ),
    )

    def parse(self, response):
        for listing in response.css(".classified-listing"):
            link = listing.css('a.car-name::attr(href)').get()
            yield response.follow(link, callback=self.parse_vehicle_description)
    
    def get_ad_title(self, response):
        title = response.css(".well h1::text").get()
        return title

    def get_vehicle_price(self, response):
        price = response.css("strong.generic-green::text").get()    
        return price

    def get_model_year(self, response):
        year = response.css(".table tr:nth-child(1) td:nth-child(1) a::text").get()
        return year

    def get_vehicle_millage(self, response):
        millage = response.css(".table tr:nth-child(1) td:nth-child(2) p::text").get()
        return millage

    def get_vehicle_fuel_type(self, response):
        fuel_type = response.css(".table tr:nth-child(1) td:nth-child(3) a::text").get()
        return fuel_type

    def get_vehicle_transmission_type(self, response):
        transmission = response.css(".table tr:nth-child(1) td:nth-child(4) a::text").get()
        return transmission

    def get_vehicle_features(self, response):
        features = []
        for li in response.css('ul.list-unstyled.car-feature-list.nomargin li'):
            features.append(li.css('::text').get().strip())
        return features 

    def get_seller_comments(self, response):
        seller_comments = response.css('h2#scroll_seller_comments+ div::text').get()
        return seller_comments

    def get_seller_name(self, response):
        seller_name = response.css(".col-md-9 h5.nomargin::text").get()
        if not seller_name:
            seller_name = response.css(".col-md-9 label[itemprop='name'] a::text").get()
        return seller_name

    def get_image_src(self, response):
        image_src = response.css(".gallery li img::attr(src)").getall()
        return image_src
        
    def get_vehicle_information(self, response):
        key_text = []
        value_text = []
        description_dict = {}

        for list_item in response.css("li.ad-data"):    
            key_text.append(list_item.css('::text').get().strip())

        for list_item in response.css("ul.list-unstyled.ul-featured.clearfix li:not(.ad-data)"):    
            value_text.append(list_item.css('::text').get().strip())

        for i in range(len(key_text)):
            description_dict[key_text[i]] = value_text[i]
        return description_dict

    def parse_vehicle_description(self, response):
        
        vehicle_ad_description = {
            'vehicle_ad_title' : self.get_ad_title(response),
            'vehicle_price' : self.get_vehicle_price(response),
            'vehicle_model_year' : self.get_model_year(response),
            'vehicle_millage' : self.get_vehicle_millage(response),
            'vehicle_fuel_type' : self.get_vehicle_fuel_type(response),
            'vehicle_transmission_type' : self.get_vehicle_transmission_type(response),
            'seller_comments' : self.get_seller_comments(response),
            'seller_name' : self.get_seller_name(response),
            'vehicle_information' : self.get_vehicle_information(response),
            'vehicle_features' : self.get_vehicle_features(response),
            'vehicle_images_src' : self.get_image_src(response)
        }      
        self.ad_descriptions.append(vehicle_ad_description)
    
    def write_ad_description_to_json(self):
        with open("Pakwheels_Used_Cars_ad.json","w") as pakwheels_json:
            json.dump(self.ad_descriptions, pakwheels_json, indent=4)

    def close(self, reason: str):
        self.write_ad_description_to_json()
        super().close(reason)
