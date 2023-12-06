import logging
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import UserContracts
from infrastructure.database.repo.base import BaseRepo


logger = logging.getLogger(__name__)


class UserContractsRepo(BaseRepo):
    async def create_contract(
            self,
            tg_id: int,
            contract_name: str,
            contract_address: str,
            contract_description: str,
    ):
        insert_stmt = (
            insert(UserContracts)
            .values(
                tg_id=tg_id,
                contract_name=contract_name,
                contract_address=contract_address,
                contract_description=contract_description,

            )
            .returning(UserContracts)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()

    async def delete_contract_by_contract_id(self, contract_id: int):
        contract_to_delete = await self.session.execute(select(UserContracts).where(UserContracts.contract_id == contract_id))
        contract_to_delete = contract_to_delete.scalars().first()

        if contract_to_delete:
            # Delete the order
            await self.session.delete(contract_to_delete)
            await self.session.commit()
        else:
            logger.info(f"Contract with ID {contract_id} not found.")

    async def get_all_contracts(self):
        query = select(UserContracts)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalars().all()

    async def get_contracts_by_tg_id(self, tg_id: int):
        query = select(UserContracts).where(UserContracts.tg_id == tg_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalars().all()

    async def get_contracts_by_contract_id(self, contract_id: int):
        query = select(UserContracts).where(UserContracts.contract_id == contract_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalars().all()

