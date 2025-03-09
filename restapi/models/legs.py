from django.db import models

class Leg(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    departure_airport = models.CharField(max_length=255)
    arrival_airport = models.CharField(max_length=255)
    departure_time = models.CharField(max_length=255)
    arrival_time = models.CharField(max_length=255)
    stops = models.IntegerField()
    airline_name = models.CharField(max_length=255)
    airline_id = models.CharField(max_length=255)
    duration_mins = models.IntegerField()

    class Meta:
        db_table = 'legs'


    def __str__(self):
        return f"{self.id}: {self.departure_airport} -> {self.arrival_airport}"
