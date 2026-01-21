from fastapi import APIRouter

# from app.presentation.api.schemas import SetBalanceRequest

router = APIRouter(prefix="/v1/balance")


# @router.post("", status_code=204)
# async def set_user_balance(
#     body: SetBalanceRequest,
#     username: str = Header(..., description="Имя пользователя", alias="X-User-Name"),
#     privilege_service: FlightService = Depends(get_flight_service),
# ) -> None:
#     return None
