from django.db import models
from .legs import Leg

class Itinerary(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    price = models.FloatField()
    agent = models.CharField(max_length=255)
    agent_rating = models.FloatField()

    class Meta:
        db_table = 'itineraries'
        verbose_name = 'Itinerary'
        verbose_name_plural = 'Itineraries'

    def __str__(self):
        return f"{self.id}: {self.agent} ({self.price}$)"

    def legs(self):
        return Leg.objects.filter(itineraryleg__itinerary=self).order_by('departure_time')
