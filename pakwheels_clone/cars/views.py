from django.views.generic import   ListView, DetailView

from .models  import Details as CarDetails


class CarsListView(ListView):
    model = CarDetails
    template_name = "cars/cars_list.html"
    context_object_name = "cars"
    paginate_by = 25

    def get_queryset(self):
        return CarDetails.objects.all().prefetch_related('images', 'features')
