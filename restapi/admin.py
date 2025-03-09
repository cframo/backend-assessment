from django.contrib import admin
from .models import Itinerary, Leg, ItineraryLeg

class LegInline(admin.StackedInline):
    model = ItineraryLeg
    extra = 0
    verbose_name = "Leg"
    verbose_name_plural = "Legs"

    fields = ('leg', 'leg_details')
    readonly_fields = ('leg_details',)

    def leg_details(self, obj):
        if obj.leg:
            return f"From: {obj.leg.departure_airport} Time: {obj.leg.departure_time} To: {obj.leg.arrival_airport} Time {obj.leg.arrival_time} | Airline: {obj.leg.airline_name} | Duration: {obj.leg.duration_mins} mins "
        return "No Leg assigned"

    leg_details.short_description = "Leg Details"

class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'price', 'agent_rating', 'get_legs')
    search_fields = ('id', 'agent')
    list_filter = ('agent', 'agent_rating')
    inlines = [LegInline]

    def get_legs(self, obj):
        legs = ItineraryLeg.objects.filter(itinerary=obj)
        return ", ".join([f"{leg.leg.departure_airport} → {leg.leg.arrival_airport}" for leg in legs])
    get_legs.short_description = "Legs"

admin.site.register(Itinerary, ItineraryAdmin)
admin.site.register(Leg)
admin.site.register(ItineraryLeg)
