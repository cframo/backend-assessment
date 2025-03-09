import re
import requests
from django.http.response import HttpResponseServerError, JsonResponse
from django.db import transaction
from restapi.models import Itinerary, Leg, ItineraryLeg

# The main idea of this service is to import all the data from the source
# save it in the SQLite database, and from this point, continue interacting with the API while providing feedback to the user about the import process.
def seedDatabase(request):
    processesMsgs = []
    try:
        rawFlights = getFlightsData()
        rawItineraries = rawFlights.get("itineraries")
        rawLegs = rawFlights.get("legs")
        processesMsgs.append(seedItineraries(rawItineraries))
        processesMsgs.append(seedLegs(rawLegs))
        processesMsgs.append(seedItineraryLegs(rawItineraries))
        transaction.commit()
    except requests.exceptions.RequestException as err:
        transaction.rollback()
        return HttpResponseServerError(str(err))
    return JsonResponse({"messages": processesMsgs})

def getFlightsData():
    baseUrl = "https://raw.githubusercontent.com/Skyscanner/full-stack-recruitment-test/main/public/flights.json"
    try:
        response = requests.get(baseUrl)
        return response.json()
    except requests.exceptions.RequestException as err:
        return None

def seedItineraries(rawItineraries):
    try:
        for itinerary in rawItineraries:
            nestedItinerary, created = Itinerary.objects.get_or_create(
                id=itinerary["id"],
                defaults={
                    "price": re.sub(r'[^\d.]', '', itinerary["price"]),
                    "agent": itinerary["agent"],
                    "agent_rating": itinerary["agent_rating"],
                }
            )
            if not created:
                nestedItinerary.price = re.sub(r'[^\d.]', '', itinerary["price"])
                nestedItinerary.agent = itinerary['agent']
                nestedItinerary.agent_rating = itinerary['agent_rating']
                nestedItinerary.save()
    except Exception as err:
        return "Something went wrong: " + str(err)
    return "Itineraries seeded"

def seedLegs(rawLegs):
    try:
        for leg in rawLegs:
            nestedLeg, created = Leg.objects.get_or_create(
                id=leg["id"],
                defaults={
                    "departure_airport": leg["departure_airport"],
                    "arrival_airport": leg["arrival_airport"],
                    "departure_time": leg["departure_time"],
                    "arrival_time": leg["arrival_time"],
                    "stops": leg["stops"],
                    "airline_name": leg["airline_name"],
                    "airline_id": leg["airline_id"],
                    "duration_mins": leg["duration_mins"],
                }
            )
            if not created:
                nestedLeg.departure_airport = leg["departure_airport"]
                nestedLeg.arrival_airport = leg["arrival_airport"]
                nestedLeg.departure_time = leg["departure_time"]
                nestedLeg.arrival_time = leg["arrival_time"]
                nestedLeg.stops = leg["stops"]
                nestedLeg.airline_name = leg["airline_name"]
                nestedLeg.airline_id = leg["airline_id"]
                nestedLeg.duration_mins = leg["duration_mins"]
    except Exception as err:
        return "Something went wrong: " + str(err)
    return "Legs seeded"

def seedItineraryLegs(rawItinerary):
    try:
        for itinerary in rawItinerary:
            for leg in itinerary['legs']:
                ItineraryLeg.objects.get_or_create(
                    itinerary = Itinerary.objects.get(id=itinerary["id"]),
                    leg = Leg.objects.get(id=leg),
                )
    except Exception as err:
        return "Something went wrong: " + str(err)
    return "ItineraryLegs seeded"