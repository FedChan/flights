from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Seat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_SEAT: _ClassVar[Seat]
    ECONOMY: _ClassVar[Seat]
    PREMIUM_ECONOMY: _ClassVar[Seat]
    BUSINESS: _ClassVar[Seat]
    FIRST: _ClassVar[Seat]

class Trip(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_TRIP: _ClassVar[Trip]
    ROUND_TRIP: _ClassVar[Trip]
    ONE_WAY: _ClassVar[Trip]
    MULTI_CITY: _ClassVar[Trip]

class Passenger(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_PASSENGER: _ClassVar[Passenger]
    ADULT: _ClassVar[Passenger]
    CHILD: _ClassVar[Passenger]
    INFANT_IN_SEAT: _ClassVar[Passenger]
    INFANT_ON_LAP: _ClassVar[Passenger]
UNKNOWN_SEAT: Seat
ECONOMY: Seat
PREMIUM_ECONOMY: Seat
BUSINESS: Seat
FIRST: Seat
UNKNOWN_TRIP: Trip
ROUND_TRIP: Trip
ONE_WAY: Trip
MULTI_CITY: Trip
UNKNOWN_PASSENGER: Passenger
ADULT: Passenger
CHILD: Passenger
INFANT_IN_SEAT: Passenger
INFANT_ON_LAP: Passenger

class Airport(_message.Message):
    __slots__ = ("airport",)
    AIRPORT_FIELD_NUMBER: _ClassVar[int]
    airport: str
    def __init__(self, airport: _Optional[str] = ...) -> None: ...

class FlightData(_message.Message):
    __slots__ = ("date", "departure_min_hour", "departure_max_hour", "arrival_min_hour", "arrival_max_hour", "max_flight_duration_minutes", "from_airport", "to_airport", "connecting_airport", "max_stops", "airlines", "min_connection_time_minutes", "max_connection_time_minutes", "less_emissions")
    DATE_FIELD_NUMBER: _ClassVar[int]
    DEPARTURE_MIN_HOUR_FIELD_NUMBER: _ClassVar[int]
    DEPARTURE_MAX_HOUR_FIELD_NUMBER: _ClassVar[int]
    ARRIVAL_MIN_HOUR_FIELD_NUMBER: _ClassVar[int]
    ARRIVAL_MAX_HOUR_FIELD_NUMBER: _ClassVar[int]
    MAX_FLIGHT_DURATION_MINUTES_FIELD_NUMBER: _ClassVar[int]
    FROM_AIRPORT_FIELD_NUMBER: _ClassVar[int]
    TO_AIRPORT_FIELD_NUMBER: _ClassVar[int]
    CONNECTING_AIRPORT_FIELD_NUMBER: _ClassVar[int]
    MAX_STOPS_FIELD_NUMBER: _ClassVar[int]
    AIRLINES_FIELD_NUMBER: _ClassVar[int]
    MIN_CONNECTION_TIME_MINUTES_FIELD_NUMBER: _ClassVar[int]
    MAX_CONNECTION_TIME_MINUTES_FIELD_NUMBER: _ClassVar[int]
    LESS_EMISSIONS_FIELD_NUMBER: _ClassVar[int]
    date: str
    departure_min_hour: int
    departure_max_hour: int
    arrival_min_hour: int
    arrival_max_hour: int
    max_flight_duration_minutes: int
    from_airport: _containers.RepeatedCompositeFieldContainer[Airport]
    to_airport: _containers.RepeatedCompositeFieldContainer[Airport]
    connecting_airport: _containers.RepeatedScalarFieldContainer[str]
    max_stops: int
    airlines: _containers.RepeatedScalarFieldContainer[str]
    min_connection_time_minutes: int
    max_connection_time_minutes: int
    less_emissions: bool
    def __init__(self, date: _Optional[str] = ..., departure_min_hour: _Optional[int] = ..., departure_max_hour: _Optional[int] = ..., arrival_min_hour: _Optional[int] = ..., arrival_max_hour: _Optional[int] = ..., max_flight_duration_minutes: _Optional[int] = ..., from_airport: _Optional[_Iterable[_Union[Airport, _Mapping]]] = ..., to_airport: _Optional[_Iterable[_Union[Airport, _Mapping]]] = ..., connecting_airport: _Optional[_Iterable[str]] = ..., max_stops: _Optional[int] = ..., airlines: _Optional[_Iterable[str]] = ..., min_connection_time_minutes: _Optional[int] = ..., max_connection_time_minutes: _Optional[int] = ..., less_emissions: bool = ...) -> None: ...

class Bags(_message.Message):
    __slots__ = ("carry_on_bags", "unknown")
    CARRY_ON_BAGS_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    carry_on_bags: int
    unknown: int
    def __init__(self, carry_on_bags: _Optional[int] = ..., unknown: _Optional[int] = ...) -> None: ...

class Info(_message.Message):
    __slots__ = ("data", "seat", "passengers", "max_price", "bags", "no_self_transfer", "trip")
    DATA_FIELD_NUMBER: _ClassVar[int]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    PASSENGERS_FIELD_NUMBER: _ClassVar[int]
    MAX_PRICE_FIELD_NUMBER: _ClassVar[int]
    BAGS_FIELD_NUMBER: _ClassVar[int]
    NO_SELF_TRANSFER_FIELD_NUMBER: _ClassVar[int]
    TRIP_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[FlightData]
    seat: Seat
    passengers: _containers.RepeatedScalarFieldContainer[Passenger]
    max_price: int
    bags: Bags
    no_self_transfer: bool
    trip: Trip
    def __init__(self, data: _Optional[_Iterable[_Union[FlightData, _Mapping]]] = ..., seat: _Optional[_Union[Seat, str]] = ..., passengers: _Optional[_Iterable[_Union[Passenger, str]]] = ..., max_price: _Optional[int] = ..., bags: _Optional[_Union[Bags, _Mapping]] = ..., no_self_transfer: bool = ..., trip: _Optional[_Union[Trip, str]] = ...) -> None: ...

class Price(_message.Message):
    __slots__ = ("price", "currency")
    PRICE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    price: int
    currency: str
    def __init__(self, price: _Optional[int] = ..., currency: _Optional[str] = ...) -> None: ...

class ItinerarySummary(_message.Message):
    __slots__ = ("flights", "price")
    FLIGHTS_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    flights: str
    price: Price
    def __init__(self, flights: _Optional[str] = ..., price: _Optional[_Union[Price, _Mapping]] = ...) -> None: ...
