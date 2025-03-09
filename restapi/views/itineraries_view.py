from pprint import pprint

from django.http.response import JsonResponse
from restapi.models import Itinerary

def index(request):

    # Here, I limit the parameters (or filters) that users can pass through API requests.
    # These limitations help ensure a single entry point, providing dynamic and user-friendly functionality.

    allowedGeneralParams = {'price', 'agent_rating', 'agent', 'id', 'duration_mins', 'stops', 'airline_name'}
    allowedItinerariesParams = {'price', 'agent_rating', 'agent', 'id'}
    allowedCompares = ['>', '<']
    innerAllowedLegsParams = {'duration_mins', 'stops', 'airline_name'}
    innerAllowedItinerariesParams = {'agent_rating', 'price'}
    params = filterParams(request.GET.dict(), allowedGeneralParams)

    if not params:
        itinerariesData = Itinerary.objects.all()
    else:
        filters = {}
        for key, value in params.items():
            if value and key in allowedItinerariesParams:
                if value[0] in allowedCompares:
                    if value[0] == ">":
                        filters[f"{key}__gt"] = float(value[1:])
                    else:
                        filters[f"{key}__lt"] = float(value[1:])
                    continue
                values = value.split(",")
                if len(values) == 1:
                    filters[f"{key}__icontains"] = values[0]
                else:
                    filters[f"{key}__in"] = values
        itinerariesData = Itinerary.objects.filter(**filters)

    formattedItineraries = [
        {
            "flight": itinerary.id,
            "agent": itinerary.agent,
            "legs": [
                {
                    f"Leg: {legIndex}": {
                        "departure_time": leg.departure_time,
                        "departure_location": leg.departure_airport,
                        'arrival_time': leg.arrival_time,
                        "arrival_location": leg.arrival_airport,
                        **({"complementary": complementaryData(params, leg, innerAllowedLegsParams)} if params else {})
                    }
                }
                for legIndex, leg in enumerate(itinerary.legs())
            ],
            **({"complementary": complementaryData(params, itinerary, innerAllowedItinerariesParams)} if params else {})
        }
        for itinerary in itinerariesData
    ]
    return JsonResponse(formattedItineraries, safe=False)

def filterParams(params, allowedParams):
    return {key: value for key, value in params.items() if key in allowedParams}

def complementaryData(params, model, innerAllowedParams):
    if not params:
        return None
    complementary = {
            param: getattr(model, param, {})
            for param in set(params) if param in innerAllowedParams
    }
    return complementary