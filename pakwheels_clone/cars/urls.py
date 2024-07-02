from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . views import CarsListView

urlpatterns = [
    path("",CarsListView.as_view(), name="cars_list"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)