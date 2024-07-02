import json


from django.core.management.base import BaseCommand, CommandError


from cars.models import CarDetails, CarModel, CarManufacturer, CarFeatures, CarImages
from users.models import User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str)

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        file = open(json_file,'r')
        used_car_data = json.load(file)
        for car_listed in used_car_data:
          self.setup_car_details(car_listed)

    def setup_car_details(self, car_listed):
        model, _ = CarModel.objects.get_or_create(car_model=car_listed['vehicle_model'])
        manufacturer, _ = CarManufacturer.objects.get_or_create(car_make=car_listed['vehicle_manufacturer'])
        user, _ = User.objects.get_or_create(name=car_listed['seller_name'])
        vehicle_information = car_listed['vehicle_information']

        car = CarDetails.objects.create(
            model=model, 
            car_make=manufacturer,
            seller=user,
            title=car_listed['vehicle_ad_title'] ,
            body_type=vehicle_information.get('Body Type', "none"),
            price=car_listed['vehicle_price'],
            year=car_listed['vehicle_model_year'],
            millage=car_listed['vehicle_millage'],
            fuel_type=car_listed['vehicle_fuel_type'],
            transmission_type=car_listed['vehicle_transmission_type'],
            registered_in=vehicle_information['Registered In'],
            color=vehicle_information['Color'],
            assembly=vehicle_information.get('Assembly', "none"),
            engine_capacity=vehicle_information.get('Engine Capacity', "none"),
            chasis_num=vehicle_information.get('Chassis No.', "none"),
            auction_num=vehicle_information.get('Auction Grade', "nonce"), 
            seller_comments=car_listed['seller_comments'],
        )
        self.add_features(car, car_listed)
        self.add_images(car, car_listed)

    def add_features(self, car, car_listed):
         for feature in car_listed['vehicle_features']:
            featur, _ = CarFeatures.objects.get_or_create(feature=feature)
            car.features.add(featur)

    def add_images(self, car, car_listed):
        for image_src in car_listed['vehicle_images_src']:
            img, _ = CarImages.objects.get_or_create(image=image_src)
            car.images.add(img)
