import random

from django.core.management.base import BaseCommand

from car_data_factory import CarModelFactory, CarDetailsFactory, UserFactory, CarFeaturesFactory, CarImagesFactory, CarManufacturerFactory


class Command(BaseCommand):

    def handle(self, *args, **kwargs):     
       for _ in range(50):
           self.setup_car_details()

    def setup_car_details(self):        
        model = CarModelFactory()
        manufacturer = CarManufacturerFactory()
        user = UserFactory()
        car = CarDetailsFactory(
            car_make=manufacturer,
            model=model, 
            seller=user,
        )
        self.add_features(car)
        self.add_images(car)

    def add_features(self, car):
         for _ in range(random.randint(1, 6)):
            feature_object = CarFeaturesFactory()
            car.features.add(feature_object)

    def add_images(self, car):
        for _ in range(random.randint(1, 4)):
            image_object = CarImagesFactory()
            car.images.add(image_object)
