from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import CarsListView

urlpatterns = [
    path("", CarsListView.as_view(), name="cars_list"),
]
