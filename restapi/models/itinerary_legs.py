from django.db import models
from .legs import Leg
from .itineraries import Itinerary

class ItineraryLeg(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    leg = models.ForeignKey(Leg, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('itinerary', 'leg')
        db_table = 'itinerary_legs'

    def __str__(self):
        return f"Itinerary {self.itinerary.id} - Leg {self.leg.id}"
