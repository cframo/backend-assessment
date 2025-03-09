from django.urls import path
from restapi.views.itineraries_view import index

urlpatterns = [
    path('', index, name='index'),
    # path('create/', create_itinerary, name='create_itinerary'), crear itinerarios
]
