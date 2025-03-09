# Flights back-end recruitment test

Thanks for taking the time to do our back-end coding test. The challenge has two parts:

1. A [task](#task) to create a flights REST API.

2. A [task](#task) to display basic flights results in the Django Administration Site.

---

## Tasks

**REST API**

- Fetch flight results from the provided `flights.json` (https://raw.githubusercontent.com/Skyscanner/full-stack-recruitment-test/main/public/flights.json) and save them into a SQLite database (or another of your choice). The models created and their relationships are up to you.
- Create an endpoint to LIST all of the flights with at least one query param to filter. The choice of the filter/filters is to be decided by your own criteria.

**Django Administration**

- Use the returned data to display a page of the fetched results in a user-friendly manner in the Django Administration. The format, columns, and all of the display details are up to you.

## Flight results

The provided (https://raw.githubusercontent.com/Skyscanner/full-stack-recruitment-test/main/public/flights.json) will return two collections of different items:

- **Itineraries** - These are the containers for your trips, tying together **Legs**, and **prices**. Prices are offered by an **agent** - an airline or travel agent.

- **Legs** - These are journeys (outbound, return) with **duration**, **stops** and **airlines**.

## Submission Guidelines

- A fork of this repository should be sent to antonio@kodealabs.com with the implemented tasks in no less than 4h of the start of the assesment. However, the assesment is expected to take about 3h. The amount of time you take to take the assesment has no effect in the results.

## Evaluation Criteria

- Your implementation works as described in the [task](#task).
- Quality of the implemented code
- Design decisions (models, JSON structure, relationships between entities, etc)
- Videocall or in-person interview to explain the implemented code to a group

---

Inspiration for the test format taken with ❤️ from [JustEat's recruitment test](https://github.com/justeat/JustEat.RecruitmentTest).

---

## Available routes

To seed database:
1. getData: **GET** - `{{localhost}}/dbmanager/getData`
  > If everything works as expected, you will receive the following JSON response: {
  "messages": [
    "Itineraries seeded",
    "Legs seeded",
    "ItineraryLegs seeded"
  ]
}
    
2. Flight (or itineraies): **GET** `{{localhost}}/itineraries/`
   1. Default (no query parameters): Retrieves all flights without additional details.
   2. You can add the following complementary data for itineraries:: 
      1. agent_rating
      2. price
   3. You can add the following complementary data for legs:
      1. stops
      2. duration_mins
      3. airline_name
   4. Search by:
      1. itinerary.**id**
      2. itinerary.**agent**
      3. itinerary.**price**
      4. itinerary.**agent_rating**
      > If a parameter is provided in the format: **id=it_2,it_1**, the API will return the records matching this pattern. _This works for all parameters_.
   5. Filters:
      1. The available comparisons are [ >, <], and work propertly with **price** and **agent_rating**
  
