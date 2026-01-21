from app.services.exceptions import UserNotFoundError, UsernameAlreadyExistError
from app.presentation.api.schemas import PrivilegeResponse
from app.infrastructure.repositories import PrivilegeRepository


class PrivilegeService:
    def __init__(self, privilege_repository: PrivilegeRepository):
        self._privilege_repository = privilege_repository

    async def create_new_user(self, username: str) -> None:
        user = await self._privilege_repository.get_user(username)

        if user is not None:
            raise UsernameAlreadyExistError(username=username)

        await self._privilege_repository.create_new_user(username)
        return

    async def delete_user(self, username: str) -> None:
        user = await self._privilege_repository.get_user(username)

        if user is None:
            raise UserNotFoundError(username=username)

        await self._privilege_repository.delete_user(username)
        return

    async def get_user(self, username: str) -> PrivilegeResponse:
        user = await self._privilege_repository.get_user(username)

        if user is None:
            raise UserNotFoundError(username=username)

        return PrivilegeResponse.model_validate(user)

    async def set_user_balance(self, username: str, balance: int) -> None:
        user = await self._privilege_repository.get_user(username)

        if user is None:
            raise UserNotFoundError(username=username)

        await self._privilege_repository.set_balance(username, balance)

    async def change_user_balance(self, username: str, balance: int) -> None:
        user = await self._privilege_repository.get_user(username)

        if user is None:
            raise UserNotFoundError(username=username)

        await self._privilege_repository.set_balance(username, int(user.balance) + balance)
