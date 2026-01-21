from app.services import FlightService
from app.infrastructure.connectors.flight import FlightConnector


async def get_flight_service() -> FlightService:
    return FlightService(FlightConnector())
