import scrapy


class UsedCarsSpider(scrapy.Spider):
    name = "pakwheels"  

    def start_requests(self):
        urls = [
            "https://www.pakwheels.com/used-cars/search/-/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        listings = response.css(".classified-listing")
        for listing in listings:
            link = listing.css('a.car-name::attr(href)').get()
            yield response.follow(link, callback=self.parse_description)

        next_page = response.css('ul.pagination.search-pagi li.next_page a::attr(href)').get()
        if next_page:
            print("page ******************************************************************************************************* : ",next_page)
            yield response.follow(next_page, callback=self.parse)


    def get_ad_title(self, response):
        title = response.css(".well h1::text").get()
        print(title)

    def get_vehicle_price(self, response):
        price = response.css("strong.generic-green::text").get()
        print(price)

    def get_model_year(self, response):
        year = response.css(".table tr:nth-child(1) td:nth-child(1) a::text").get()
        print(year)

    def get_vehicle_millage(self, response):
        millage = response.css(".table tr:nth-child(1) td:nth-child(2) p::text").get()
        print(millage)

    def get_vehicle_fuel_type(self, response):
        fuel_type = response.css(".table tr:nth-child(1) td:nth-child(3) a::text").get()
        print(fuel_type)

    def get_vehicle_transmission_type(self, response):
        transmission = response.css(".table tr:nth-child(1) td:nth-child(4) a::text").get()
        print(transmission)

    def get_vehicle_features(self, response):
        for li in response.css('ul.list-unstyled.car-feature-list.nomargin li'):
            feature = li.css('::text').get().strip()
            print(feature,end=",")

    def get_seller_comments(self, response):
        seller_comments = response.css('h2#scroll_seller_comments+ div::text').get()
        print(f"\n{seller_comments.strip()}")

    def get_seller_name(self, response):
        seller_name = response.css("h5.nomargin::text").get()
        print(seller_name)

    def get_image_src(self, response):
        image_src = response.css(".gallery li img::attr(src)").getall()
        print(image_src)
        


    def get_vehicle_description(self, response):
        description_li_elements = response.css('ul.list-unstyled.ul-featured.clearfix li')
        description_dict = {}
        for li in range(0, len(description_li_elements)-1, 2):
            key_text = description_li_elements[li].css('::text').get().strip()
            value_text = description_li_elements[li + 1].css('::text').get().strip()
            description_dict[key_text] = value_text
        print(description_dict)


    def parse_description(self, response):
        
        self.get_ad_title(response)
        self.get_vehicle_price(response)
        self.get_model_year(response)
        self.get_vehicle_millage(response)
        self.get_vehicle_fuel_type(response)
        self.get_vehicle_transmission_type(response)
        self.get_vehicle_features(response)
        self.get_seller_comments(response)
        self.get_seller_name(response)
        self.get_image_src(response)
        self.get_vehicle_description(response)
