import factory.faker

from factory.django import DjangoModelFactory
import factory.random
from faker import Faker
from faker_vehicle import VehicleProvider

from cars.models import Details, CarModel, Manufacturer, Features, Images
from users.models import User

faker = Faker()
faker.add_provider(VehicleProvider)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('phone_number',)
  
    phone_number = factory.Faker('phone_number')


class CarModelFactory(DjangoModelFactory):
    class Meta:
        model = CarModel
        django_get_or_create = ('car_model',)

    car_model = factory.lazy_attribute(lambda _: faker.vehicle_model())


class CarManufacturerFactory(DjangoModelFactory):
    class Meta:
        model = Manufacturer
        django_get_or_create = ('car_make',)

    car_make = factory.LazyAttribute(lambda _: faker.vehicle_make())


class CarFeaturesFactory(DjangoModelFactory):
    class Meta:
        model = Features
        django_get_or_create = ('feature',)

    feature = factory.Faker('random_element', elements=[
        'Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 
        'Airbags', 'Sunroof', 'Alloy Wheels', 'Navigation System',
        'Bluetooth', 'Backup Camera', 'Cruise Control'
    ])


class CarImagesFactory(DjangoModelFactory):
    class Meta:
        model = Images
        django_get_or_create = ('image',)

    image = factory.django.ImageField(color=factory.Faker('color_name'))


class CarDetailsFactory(DjangoModelFactory):
    class Meta:
        model = Details
    
    model = factory.SubFactory(CarModelFactory)
    car_make = factory.SubFactory(CarManufacturerFactory)
    seller = factory.SubFactory(UserFactory)

    price = factory.Faker('pyint', min_value=500000, max_value=50000000)
    millage = factory.Faker('pyint', min_value=1, max_value=200000)
    registered_in = factory.Faker('city')
    color = factory.Faker('color_name')
    seller_comments = factory.Faker('text')

    engine_capacity = factory.Faker('random_element', elements=[
        '1000 CC', '1300 CC', '1500 CC', 
        '1800 CC', '2000 CC', '2500 CC',
        ])
    
    fuel_type = factory.Faker('random_element', elements=[
        'Petrol', 'Diesel'
        ])
    
    transmission_type = factory.Faker('random_element', elements=[
        'Automatic', 'Manual'
        ])
    
    assembly = factory.Faker('random_element', elements=[
        'Local', 'Imported'
        ])

    year = factory.lazy_attribute(lambda _: faker.vehicle_year())
