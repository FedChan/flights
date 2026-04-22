import json
import re

from selectolax.lexbor import LexborHTMLParser

from .model import (
    Airline,
    Airport,
    Alliance,
    CarbonEmission,
    Flights,
    JsMetadata,
    SimpleDatetime,
    SingleFlight,
)


class MetaList(list[Flights]):
    """Searched flights list, with metadata attached."""

    metadata: JsMetadata


def parse(html: str) -> MetaList:
    parser = LexborHTMLParser(html)

    total_durations = re.findall(r"aria-label=.Total duration (.*?)\.", html)

    # find js
    script = parser.css_first(r"script.ds\:1")
    return parse_js(script.text(), total_durations)


# Data discovery by @kftang, huge shout out!
def parse_js(js: str, total_durations: list[str]):
    data = js.split("data:", 1)[1].rsplit(",", 1)[0]
    # print(data)

    payload = json.loads(data)

    # import ipdb; ipdb.set_trace()

    alliances = []
    airlines = []

    (alliances_data, airlines_data) = (
        payload[7][1][0],
        payload[7][1][1],
    )

    for code, name in alliances_data:
        alliances.append(Alliance(code=code, name=name))

    for code, name in airlines_data:
        airlines.append(Airline(code=code, name=name))

    meta = JsMetadata(alliances=alliances, airlines=airlines)

    flights = MetaList()
    if payload[3][0] is None:
        return flights

    for k, total_duration in zip(payload[3][0], total_durations):
        flight = k[0]
        price = k[1][0][1]

        typ = flight[0]
        airlines = flight[1]

        sg_flights = []

        # multiple flights!
        for single_flight in flight[2]:
            from_airport = Airport(code=single_flight[3], name=single_flight[4])
            to_airport = Airport(code=single_flight[6], name=single_flight[5])
            departure_time = single_flight[8]
            departure_date = single_flight[20]
            if len(departure_time) == 1:
                departure_time += [0]
            departure_time = [0 if val is None else val for val in departure_time]
            departure = SimpleDatetime(date=departure_date, time=departure_time)

            arrival_time = single_flight[10]
            arrival_date = single_flight[21]
            if len(arrival_time) == 1:
                arrival_time += [0]
            arrival_time = [0 if val is None else val for val in departure_time]
            arrival = SimpleDatetime(date=arrival_date, time=arrival_time)

            if departure_time[0] is None or arrival_time[0] is None:
                import ipdb; ipdb.set_trace()

            plane_type = single_flight[17]

            duration = single_flight[11]

            sg_flights.append(
                SingleFlight(
                    from_airport=from_airport,
                    to_airport=to_airport,
                    departure=departure,
                    arrival=arrival,
                    duration=duration,
                    plane_type=plane_type,
                )
            )

        # some additional data
        extras = flight[22]
        carbon_emission = extras[7]
        typical_carbon_emission = extras[8]

        flights.append(
            Flights(
                type=typ,
                price=price,
                airlines=airlines,
                flights=sg_flights,
                carbon=CarbonEmission(
                    typical_on_route=typical_carbon_emission, emission=carbon_emission
                ),
                total_duration=total_duration,
            )
        )

    flights.metadata = meta
    return flights
