from django.contrib import admin
from django.db import models


from users.models import User


class CarManufacturer(models.Model):
    car_make = models.CharField(max_length=50)


class CarModel(models.Model):
    car_model = models.CharField(max_length=150)


class CarFeatures(models.Model):
    feature = models.CharField(max_length=200)


class CarImages(models.Model):
    image = models.ImageField(upload_to="images")


class CarDetails(models.Model):
    fuel_choices = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
    ]
    transmission_choices = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]
    assembly_choices = [
        ('Local','Local'),
        ('Imported','Imported'),
    ]
    title = models.CharField(max_length=100)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    car_make = models.ForeignKey(CarManufacturer, on_delete=models.CASCADE)
    features = models.ManyToManyField(CarFeatures)
    body_type = models.CharField(max_length=50)
    price = models.CharField(max_length=20, null=True)
    year = models.IntegerField(null=True)
    millage = models.CharField(max_length=20, null=True)
    fuel_type = models.CharField(max_length=50, choices=fuel_choices, null=True)
    transmission_type = models.CharField(max_length=50, choices=transmission_choices, null=True)
    registered_in = models.CharField(max_length=50, null=True)
    color = models.CharField(max_length=50, null=True)
    assembly = models.CharField(max_length=50, choices=assembly_choices, null=True)
    engine_capacity = models.CharField(max_length=50, null=True)
    images = models.ManyToManyField(CarImages, blank=True)
    chasis_num = models.CharField(max_length=50, blank=True, null=True)
    auction_num = models.CharField(max_length=50, blank=True, null=True)
    ad_created = models.DateTimeField(auto_now_add=True)
    ad_last_updated = models.DateTimeField(auto_now=True)
    seller_comments = models.TextField(blank=True)
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
