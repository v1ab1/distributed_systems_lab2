from typing import cast

from sqlalchemy import Column, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.privilege import PrivilegeDB


class PrivilegeRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create_new_user(self, username: str) -> int:
        person_db = PrivilegeDB(username=username)
        self._db.add(person_db)
        await self._db.flush()
        person_id = person_db.id
        await self._db.commit()
        return int(person_id)

    async def get_user(self, username: str) -> PrivilegeDB | None:
        query = select(PrivilegeDB).where(PrivilegeDB.username == username)
        result = await self._db.execute(query)
        person = result.scalar_one_or_none()

        return person

    async def delete_user(self, username: str) -> None:
        await self._db.execute(delete(PrivilegeDB).where(PrivilegeDB.username == username))
        await self._db.commit()

    async def set_balance(self, username: str, balance: int) -> None:
        user = await self.get_user(username)
        if user is None:
            return
        user.balance = cast(Column[int], balance)
        await self._db.commit()
        await self._db.refresh(user)
