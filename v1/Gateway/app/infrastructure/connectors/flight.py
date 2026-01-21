import os
from urllib.parse import urljoin

from dotenv import load_dotenv
import httpx

from app.presentation.api.schemas import AllFlightsResponse

load_dotenv(override=True)
flight_service_url = os.getenv("FLIGHT_SERVICE_URL", "")


class FlightConnector:
    def get_flights(self, page: int, size: int) -> AllFlightsResponse:
        with httpx.Client(verify=False) as client:
            response = client.get(urljoin(flight_service_url, '/v1/flights'), params={"page": page, "size": size})
            response_json = response.json()
            return AllFlightsResponse.model_validate(response_json)
