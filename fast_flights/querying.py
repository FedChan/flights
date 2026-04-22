from base64 import b64encode
from dataclasses import dataclass
from datetime import datetime as Datetime
from typing import Literal, Optional, Union

from .pb.flights_pb2 import Airport, FlightData, Info, Passenger, Seat, Trip, Bags
from .types import Currency, Language, SeatType, TripType


@dataclass
class Query:
    """A query containing `?tfs` data."""

    flight_data: list[FlightData]
    seat: Seat
    trip: Trip
    passengers: list[Passenger]
    language: str
    currency: str
    max_price: int | None = None
    bags: Bags | None = Bags(carry_on_bags=0, unknown=0)
    no_self_transfer: bool | None = None

    def pb(self) -> Info:
        """(internal) Protobuf data. (`Info`)"""
        return Info(
            data=self.flight_data,
            seat=self.seat,
            trip=self.trip,
            passengers=self.passengers,
            max_price=self.max_price,
            bags=self.bags,
            no_self_transfer=self.no_self_transfer,
        )

    def to_bytes(self) -> bytes:
        """Convert this query to bytes."""
        return self.pb().SerializeToString()

    def to_str(self) -> str:
        """Convert this query to a string."""
        return b64encode(self.to_bytes()).decode("utf-8")

    def url(self) -> str:
        """Get the URL for this query.

        This is generally used for debugging purposes.
        """
        return (
            "https://www.google.com/travel/flights/search?tfs="
            + self.to_str()
            + "&hl="
            + self.language
            + "&curr="
            + self.currency
        )

    def params(self) -> dict[str, str]:
        """Create `params` in dictionary form."""
        return {"tfs": self.to_str(), "hl": self.language, "curr": self.currency}

    def __repr__(self) -> str:
        return "Query(...)"


@dataclass
class FlightQuery:
    date: str | Datetime
    from_airport: str
    to_airport: str
    max_stops: int | None = None
    airlines: list[str] | None = None
    departure_min_hour: int | None = None
    departure_max_hour: int | None = None
    arrival_min_hour: int | None = None
    arrival_max_hour: int | None = None
    max_flight_duration_minutes: int | None = None
    connecting_airport: list[str] | None = None
    min_connection_time_minutes: int | None = None
    max_connection_time_minutes: int | None = None
    less_emissions: bool | None = None

    def pb(self) -> FlightData:
        if isinstance(self.date, str):
            date = self.date
        else:
            date = self.date.strftime("%Y-%m-%d")

        from_airports = []
        for airport in self.from_airport.split(","):
            from_airports.append(Airport(airport=airport))

        to_airports = []
        for airport in self.to_airport.split(","):
            to_airports.append(Airport(airport=airport))

        return FlightData(
            date=date,
            from_airport=from_airports,
            to_airport=to_airports,
            max_stops=self.max_stops,
            airlines=self.airlines,
            departure_min_hour = self.departure_min_hour,
            departure_max_hour = self.departure_max_hour,
            arrival_min_hour = self.arrival_min_hour,
            arrival_max_hour = self.arrival_max_hour,
            max_flight_duration_minutes = self.max_flight_duration_minutes,
            connecting_airport = self.connecting_airport,
            min_connection_time_minutes = self.min_connection_time_minutes,
            max_connection_time_minutes = self.max_connection_time_minutes,
            less_emissions = self.less_emissions,
        )

    def _setmaxstops(self, m: int | None = None) -> "FlightQuery":
        if m is not None:
            self.max_stops = m

        return self


class Passengers:
    def __init__(
        self,
        *,
        adults: int = 0,
        children: int = 0,
        infants_in_seat: int = 0,
        infants_on_lap: int = 0,
    ):
        assert sum((adults, children, infants_in_seat, infants_on_lap)) <= 9, (
            "Too many passengers (> 9)"
        )
        assert infants_on_lap <= adults, (
            "Must have at least one adult per infant on lap"
        )

        self.adults = adults
        self.children = children
        self.infants_in_seat = infants_in_seat
        self.infants_on_lap = infants_on_lap

    def pb(self) -> list[Passenger]:
        return [
            *(Passenger.ADULT for _ in range(self.adults)),
            *(Passenger.CHILD for _ in range(self.children)),
            *(Passenger.INFANT_IN_SEAT for _ in range(self.infants_in_seat)),
            *(Passenger.INFANT_ON_LAP for _ in range(self.infants_on_lap)),
        ]


DEFAULT_PASSENGERS = Passengers(adults=1)
SEAT_LOOKUP = {
    "economy": Seat.ECONOMY,
    "premium-economy": Seat.PREMIUM_ECONOMY,
    "business": Seat.BUSINESS,
    "first": Seat.FIRST,
}
TRIP_LOOKUP = {
    "round-trip": Trip.ROUND_TRIP,
    "one-way": Trip.ONE_WAY,
    "multi-city": Trip.MULTI_CITY,
}


def create_query(
    *,
    flights: list[FlightQuery],
    seat: SeatType = "economy",
    trip: TripType = "one-way",
    passengers: Passengers = DEFAULT_PASSENGERS,
    language: str | Literal[""] | Language = "",
    currency: str | Literal[""] | Currency = "",
    max_stops: int | None = None,
    max_price: int | None = None,
    carry_on_bags: int | None = None,
    no_self_transfer: bool | None = None,
) -> Query:
    """Create a query.

    Args:
        flights: The flight queries.
        seat: Desired seat type.
        trip: Trip type.
        passengers: Passengers.
        language: Set the language. Use `""` (blank str) to let Google decide.
        currency: Set the currency. Use `""` (blank str) to let Google decide.
        max_stops (optional): Set the maximum stops for every flight query, if present.
        max_price (optional): Set the maximum price for the trip.
        carry_on_bags (optional): Set the amount of carry-on bags.
        no_self_transfer (optional): Set whether to exclude self-transfer in connecting flights.
    """
    return Query(
        flight_data=[flight._setmaxstops(max_stops).pb() for flight in flights],
        seat=SEAT_LOOKUP[seat],
        trip=TRIP_LOOKUP[trip],
        passengers=passengers.pb(),
        language=language,
        currency=currency,
        max_price=max_price,
        bags=Bags(carry_on_bags=carry_on_bags, unknown=0),
        no_self_transfer=no_self_transfer,
    )
