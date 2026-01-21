from app.db.models.flight import FlightDB
from app.services.exceptions import FlightNotFoundError
from app.presentation.api.schemas import FlightMeta, FlightResponse
from app.infrastructure.repositories.flight import FlightRepository


class FlightService:
    def __init__(self, flight_repository: FlightRepository):
        self._flight_repository = flight_repository

    async def get_by_id(self, id: int) -> FlightResponse:
        flight_db = await self._flight_repository.get_by_id(id)
        if flight_db is None:
            raise FlightNotFoundError(id)
        flight = FlightResponse.model_validate(flight_db)
        return flight

    async def get_all(self) -> list[FlightResponse]:
        flights_db = await self._flight_repository.get_all()
        flights = [FlightResponse.model_validate(person) for person in flights_db]
        return flights

    async def save_new_flight(self, flight: FlightMeta) -> int:
        flight_db = FlightDB(**flight.model_dump())
        return await self._flight_repository.save_new_flight(flight_db)

    async def update_flight(self, id: int, flight: FlightMeta) -> None:
        flight_db = await self._flight_repository.get_by_id(id)
        if flight_db is None:
            raise FlightNotFoundError(id)
        await self._flight_repository.update_flight(id, flight)

    async def delete_flight(self, id: int) -> None:
        flight_db = await self._flight_repository.get_by_id(id)
        if flight_db is None:
            raise FlightNotFoundError(id)
        await self._flight_repository.delete_flight(id)
