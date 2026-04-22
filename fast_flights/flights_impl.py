"""Typed implementation of flights_pb2.py"""

import base64
from dataclasses import dataclass
from typing import Any, List, Optional, TYPE_CHECKING, Literal, Union

from . import flights_pb2 as PB
from ._generated_enum import Airport

if TYPE_CHECKING:
    PB: Any

AIRLINE_ALLIANCES = ["SKYTEAM", "STAR_ALLIANCE", "ONEWORLD"]

class Bags:
    """Represents carry-on bags.
    
    Args:
        carry_on_bags (int, optional): Number of carry-on bags. Default is 0.
        unknown (int, optional): An unknown field (field 3). Default is 0.
    """
    
    __slots__ = ("carry_on_bags", "unknown")
    carry_on_bags: int
    unknown: int

    def __init__(
        self,
        *,
        carry_on_bags: int = 0,
        unknown: int = 0,
    ):
        self.carry_on_bags = carry_on_bags
        self.unknown = unknown
        
    def attach(self, info: PB.Info) -> None:  # type: ignore
        bags_pb = info.bags
        bags_pb.carry_on_bags = self.carry_on_bags
        bags_pb.unknown = self.unknown

    def __repr__(self) -> str:
        return f"Bags(carry_on_bags={self.carry_on_bags!r}, unknown={self.unknown!r})"


class FlightData:
    """Represents flight data.

    Args:
        date (str): Date.
        from_airport (str): Departure (airport). Where from?
        to_airport (str): Arrival (airport). Where to?
        airlines (list(str), optional): A list of airlines. Default is None.
        max_stops (int, optional): Maximum number of stops. Default is None.
        departure_min_hour (int, optional): Minimum departure hour (0-23).
        departure_max_hour (int, optional): Maximum departure hour (0-23, one less than the max time hour).
        arrival_min_hour (int, optional): Minimum arrival hour (0-23).
        arrival_max_hour (int, optional): Maximum arrival hour (0-23, one less than the max time hour).
        max_flight_duration_minutes (int, optional): Maximum total flight duration.
        connecting_airport (List[str], optional): List of required connecting airports.
        min_connection_time_minutes (int, optional): Minimum layover time.
        max_connection_time_minutes (int, optional): Maximum layover time.
        less_emissions (bool, optional): Flag to prefer flights with less emissions.
    """

    __slots__ = (
        "date", "from_airport", "to_airport", "max_stops", "airlines",
        "departure_min_hour", "departure_max_hour", "arrival_min_hour", "arrival_max_hour",
        "max_flight_duration_minutes", "connecting_airport",
        "min_connection_time_minutes", "max_connection_time_minutes", "less_emissions"
    )
    date: str
    from_airport: List[str]
    to_airport: List[str]
    airlines: Optional[List[str]]
    max_stops: Optional[int]
    departure_min_hour: Optional[int]
    departure_max_hour: Optional[int]
    arrival_min_hour: Optional[int]
    arrival_max_hour: Optional[int]
    max_flight_duration_minutes: Optional[int]
    connecting_airport: Optional[List[str]]
    min_connection_time_minutes: Optional[int]
    max_connection_time_minutes: Optional[int]
    less_emissions: Optional[bool]

    def __init__(
        self,
        *,
        date: str,
        from_airport: Union[Airport, str],
        to_airport: Union[Airport, str],
        airlines: Optional[List[str]] = None,
        max_stops: Optional[int] = None,
        departure_min_hour: Optional[int] = None,
        departure_max_hour: Optional[int] = None,
        arrival_min_hour: Optional[int] = None,
        arrival_max_hour: Optional[int] = None,
        max_flight_duration_minutes: Optional[int] = None,
        connecting_airport: Optional[List[str]] = None,
        min_connection_time_minutes: Optional[int] = None,
        max_connection_time_minutes: Optional[int] = None,
        less_emissions: Optional[bool] = None,
    ):
        self.date = date
        self.from_airport = (
            from_airport.value if isinstance(from_airport, Airport) else from_airport
        ).split(',')
        self.to_airport = (
            to_airport.value if isinstance(to_airport, Airport) else to_airport
        ).split(',')
        self.airlines = airlines
        self.max_stops = max_stops
        self.departure_min_hour = departure_min_hour
        self.departure_max_hour = departure_max_hour
        self.arrival_min_hour = arrival_min_hour
        self.arrival_max_hour = arrival_max_hour
        self.max_flight_duration_minutes = max_flight_duration_minutes
        self.connecting_airport = connecting_airport
        self.min_connection_time_minutes = min_connection_time_minutes
        self.max_connection_time_minutes = max_connection_time_minutes
        self.less_emissions = less_emissions

        # TODO: All the list of airlines should technically be added to ._generated_enum like Airports
        # but I don't know how to find the comprehensive list of airlines now.
        if airlines is not None:
            self.airlines = []
            for airline in airlines:
                airline = airline.upper()
                if not (len(airline) == 2 or airline in AIRLINE_ALLIANCES):
                    raise ValueError(
                        f"Invalid airline code: {airline}. "
                        f"Airline codes should be 2 characters long or in the list of airline alliances: {AIRLINE_ALLIANCES}"
                    )
                self.airlines.append(airline)
        else:
            # make it consistent with self.max_stops and set it to None
            self.airlines = None

    def attach(self, info: PB.Info) -> None:  # type: ignore
        data = info.data.add()
        data.date = self.date
        for from_airport in self.from_airport:
            data.from_flight.add().airport = from_airport
        for to_airport in self.to_airport:
            data.to_flight.add().airport = to_airport
        if self.airlines is not None:
            data.airlines.extend(self.airlines)        
        if self.max_stops is not None:
            data.max_stops = self.max_stops
        if self.departure_min_hour is not None:
            data.departure_min_hour = self.departure_min_hour
        if self.departure_max_hour is not None:
            data.departure_max_hour = self.departure_max_hour
        if self.arrival_min_hour is not None:
            data.arrival_min_hour = self.arrival_min_hour
        if self.arrival_max_hour is not None:
            data.arrival_max_hour = self.arrival_max_hour
        if self.max_flight_duration_minutes is not None:
            data.max_flight_duration_minutes = self.max_flight_duration_minutes
        if self.connecting_airport is not None:
            data.connecting_airport.extend(self.connecting_airport)
        if self.min_connection_time_minutes is not None:
            data.min_connection_time_minutes = self.min_connection_time_minutes
        if self.max_connection_time_minutes is not None:
            data.max_connection_time_minutes = self.max_connection_time_minutes
        if self.less_emissions is not None:
            data.less_emissions = self.less_emissions

    def __repr__(self) -> str:
        return (
            f"FlightData(date={self.date!r}, "
            f"from_airport={self.from_airport!r}, "
            f"to_airport={self.to_airport!r}, "
            f"airlines={self.airlines!r}, "
            f"max_stops={self.max_stops!r}, "
            f"departure_min_hour={self.departure_min_hour!r}, "
            f"departure_max_hour={self.departure_max_hour!r}, "
            f"arrival_min_hour={self.arrival_min_hour!r}, "
            f"arrival_max_hour={self.arrival_max_hour!r}, "
            f"max_flight_duration_minutes={self.max_flight_duration_minutes!r}, "
            f"connecting_airport={self.connecting_airport!r}, "
            f"min_connection_time_minutes={self.min_connection_time_minutes!r}, "
            f"max_connection_time_minutes={self.max_connection_time_minutes!r}, "
            f"less_emissions={self.less_emissions!r})"
        )


class Passengers:
    def __init__(
        self,
        *,
        adults: int = 0,
        children: int = 0,
        infants_in_seat: int = 0,
        infants_on_lap: int = 0,
    ):
        assert (
            sum((adults, children, infants_in_seat, infants_on_lap)) <= 9
        ), "Too many passengers (> 9)"
        assert (
            infants_on_lap <= adults
        ), "You must have at least one adult per infant on lap"

        self.pb = []
        self.pb += [PB.Passenger.ADULT for _ in range(adults)]
        self.pb += [PB.Passenger.CHILD for _ in range(children)]
        self.pb += [PB.Passenger.INFANT_IN_SEAT for _ in range(infants_in_seat)]
        self.pb += [PB.Passenger.INFANT_ON_LAP for _ in range(infants_on_lap)]

        self._data = (adults, children, infants_in_seat, infants_on_lap)

    def attach(self, info: PB.Info) -> None:  # type: ignore
        for p in self.pb:
            info.passengers.append(p)

    def __repr__(self) -> str:
        return f"Passengers({self._data})"


class TFSData:
    """``?tfs=`` data. (internal)

    Use `TFSData.from_interface` instead.
    """

    def __init__(
        self,
        *,
        flight_data: List[FlightData],
        seat: PB.Seat,  # type: ignore
        trip: PB.Trip,  # type: ignore
        passengers: Passengers,
        max_stops: Optional[int] = None,
        max_price: Optional[int] = None,
        bags: Optional[Bags] = None,
        no_self_transfer: Optional[bool] = None,
    ):
        self.flight_data = flight_data
        self.seat = seat
        self.trip = trip
        self.passengers = passengers
        self.max_stops = max_stops
        self.max_price = max_price
        self.bags = bags
        self.no_self_transfer = no_self_transfer

    def pb(self) -> PB.Info:  # type: ignore
        info = PB.Info()
        info.seat = self.seat
        info.trip = self.trip

        self.passengers.attach(info)

        for fd in self.flight_data:
            fd.attach(info)

        # If max_stops is set, attach it to all flight data entries
        if self.max_stops is not None:
            for flight in info.data:
                flight.max_stops = self.max_stops
        if self.max_price is not None:
            info.max_price = self.max_price
        if self.bags is not None:
            self.bags.attach(info)
        if self.no_self_transfer is not None:
            info.no_self_transfer = self.no_self_transfer

        return info

    def to_string(self) -> bytes:
        return self.pb().SerializeToString()

    def as_b64(self) -> bytes:
        return base64.b64encode(self.to_string())

    @staticmethod
    def from_interface(
        *,
        flight_data: List[FlightData],
        trip: Literal["round-trip", "one-way", "multi-city"],
        passengers: Passengers,
        seat: Literal["economy", "premium-economy", "business", "first"],
        max_stops: Optional[int] = None,
        max_price: Optional[int] = None,
        bags: Optional[Bags] = None,
        no_self_transfer: Optional[bool] = None,
    ):
        """Use ``?tfs=`` from an interface.

        Args:
            flight_data (list[FlightData]): Flight data as a list.
            trip ("one-way" | "round-trip" | "multi-city"): Trip type.
            passengers (Passengers): Passengers.
            seat ("economy" | "premium-economy" | "business" | "first"): Seat.
            max_stops (int, optional): Maximum number of stops.
            max_price (int, optional): Maximum total price.
            bags (Bags, optional): Baggage information.
            no_self_transfer (bool, optional): If set, exclude flights that require self-transfer.
        """
        trip_t = {
            "round-trip": PB.Trip.ROUND_TRIP,
            "one-way": PB.Trip.ONE_WAY,
            "multi-city": PB.Trip.MULTI_CITY,
        }[trip]
        seat_t = {
            "economy": PB.Seat.ECONOMY,
            "premium-economy": PB.Seat.PREMIUM_ECONOMY,
            "business": PB.Seat.BUSINESS,
            "first": PB.Seat.FIRST,
        }[seat]

        return TFSData(
            flight_data=flight_data,
            seat=seat_t,
            trip=trip_t,
            passengers=passengers,
            max_stops=max_stops,
            max_price=max_price,
            bags=bags,
            no_self_transfer=no_self_transfer,
        )

    def __repr__(self) -> str:
        return (
            f"TFSData(flight_data={self.flight_data!r}, "
            f"max_stops={self.max_stops!r}, "
            f"max_price={self.max_price!r})"
        )

@dataclass
class ItinerarySummary:
    flights: str
    price: int
    currency: str

    @classmethod
    def from_b64(cls, b64_string: str) -> 'ItinerarySummary':
        raw = base64.b64decode(b64_string)
        pb = PB.ItinerarySummary()
        pb.ParseFromString(raw)
        return cls(pb.flights, pb.price.price / 100, pb.price.currency)
