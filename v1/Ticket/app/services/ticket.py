import uuid

from app.services.enums import TicketStatus
from app.db.models.ticket import TicketDB
from app.services.exceptions import TicketNotFoundError
from app.presentation.api.schemas import TicketMeta, TicketResponse, TicketCreateRequest
from app.infrastructure.connectors.gateway import GatewayConnector
from app.infrastructure.repositories.ticket import TicketRepository


class TicketService:
    def __init__(self, ticket_repository: TicketRepository, gateway_connector: GatewayConnector):
        self._ticket_repository = ticket_repository
        self._gateway_connector = gateway_connector

    async def get_by_ticket_uid(self, ticket_uid: str) -> TicketResponse:
        ticket_db = await self._ticket_repository.get_by_ticket_uid(ticket_uid)
        if ticket_db is None:
            raise TicketNotFoundError(ticket_uid)
        ticket = TicketResponse.model_validate(ticket_db)
        return ticket

    async def get_all(self, page: int = 1, size: int = 10) -> tuple[list[TicketResponse], int]:
        tickets_db, total_elements = await self._ticket_repository.get_all(page, size)
        tickets = [TicketResponse.model_validate(ticket) for ticket in tickets_db]
        return tickets, total_elements

    async def get_by_username(self, username: str, page: int = 1, size: int = 10) -> tuple[list[TicketResponse], int]:
        tickets_db, total_elements = await self._ticket_repository.get_by_username(username, page, size)
        tickets = [TicketResponse.model_validate(ticket) for ticket in tickets_db]
        return tickets, total_elements

    async def save_new_ticket(self, ticket: TicketCreateRequest) -> str:
        flight = await self._gateway_connector.find_flight_by_number(ticket.flight_number)
        ticket_data = {
            "username": ticket.username,
            "flight_number": ticket.flight_number,
            "price": flight.price,
            "status": TicketStatus.PAID.value,
            "ticket_uid": uuid.uuid4(),
        }
        ticket_db = TicketDB(**ticket_data)
        return await self._ticket_repository.save_new_ticket(ticket_db)

    async def cancel_ticket(self, ticket_uid: str) -> None:
        ticket_db = await self._ticket_repository.get_by_ticket_uid(ticket_uid)
        if ticket_db is None:
            raise TicketNotFoundError(ticket_uid)
        await self._ticket_repository.cancel_ticket(ticket_uid)

    async def get_flights(self, page: int = 1, size: int = 10):
        return await self._gateway_connector.get_flights(page, size)
