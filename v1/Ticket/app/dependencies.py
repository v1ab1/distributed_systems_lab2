from app.services import TicketService
from app.db.engine import get_db
from app.infrastructure.repositories import TicketRepository
from app.infrastructure.connectors.gateway import GatewayConnector


async def get_ticket_service() -> TicketService:  # type: ignore
    async for session in get_db():
        ticket_repository = TicketRepository(session)
        gateway_connector = GatewayConnector()

        return TicketService(ticket_repository, gateway_connector)
