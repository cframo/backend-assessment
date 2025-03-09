from django.urls import path
from restapi.views.dbconnection_view import *

urlpatterns = [
    path('getData/', seedDatabase),
]
