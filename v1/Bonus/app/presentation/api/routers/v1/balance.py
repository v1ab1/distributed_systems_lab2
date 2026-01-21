from fastapi import Header, Depends, APIRouter

from app.dependencies import get_privilege_service
from app.services.privilege import PrivilegeService
from app.presentation.api.schemas import SetBalanceRequest

router = APIRouter(prefix="/v1/balance")


@router.post("", status_code=204)
async def set_user_balance(
    body: SetBalanceRequest,
    username: str = Header(..., description="Имя пользователя", alias="X-User-Name"),
    privilege_service: PrivilegeService = Depends(get_privilege_service),
) -> None:
    await privilege_service.set_user_balance(username, body.balance)


@router.put("", status_code=204)
async def change_user_balance(
    body: SetBalanceRequest,
    username: str = Header(..., description="Имя пользователя", alias="X-User-Name"),
    privilege_service: PrivilegeService = Depends(get_privilege_service),
) -> None:
    await privilege_service.change_user_balance(username, body.balance)
