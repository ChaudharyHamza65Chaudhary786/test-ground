from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class Manufacturer(models.Model):
    car_make = models.CharField(max_length=50)

    def __str__(self):
        return self.car_make


class CarModel(models.Model):
    car_model = models.CharField(max_length=150)

    def __str__(self):
        return self.car_model


class Features(models.Model):
    feature = models.CharField(max_length=200)


class Images(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m/%d")


class Details(models.Model):
    class FuelChoices(models.TextChoices):
        PETROL = "Petrol", _("Petrol")
        DIESEL = "Diesel", _("Diesel")
    
    class TransmissionChoices(models.TextChoices):
        MANUAL = "Manual", _("Manual")
        AUTOMATIC = "Automatic", _("Automatic")
    
    class AssemblyChoices(models.TextChoices):
        LOCAL = "Local", _("Local")
        IMPORTED = "Imported", _("Imported")

    assembly = models.CharField(max_length=50, choices=AssemblyChoices.choices, null=True)
    color = models.CharField(max_length=50, null=True)
    engine_capacity = models.CharField(max_length=50, null=True)
    fuel_type = models.CharField(max_length=50, choices=FuelChoices.choices, null=True)
    millage = models.CharField(max_length=20, null=True)
    price = models.CharField(max_length=20, null=True)
    registered_in = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=100)
    transmission_type = models.CharField(max_length=50, choices=TransmissionChoices.choices, null=True)

    ad_created = models.DateTimeField(auto_now_add=True)
    ad_last_updated = models.DateTimeField(auto_now=True)

    car_make = models.ForeignKey("Manufacturer", on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    seller = models.ForeignKey(User,on_delete=models.CASCADE)

    year = models.IntegerField(null=True)

    images = models.ManyToManyField(Images, blank=True)
    features = models.ManyToManyField(Features)

    seller_comments = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.title = f"{self.car_make} {self.model} {self.year}"
        super().save(*args, **kwargs)

