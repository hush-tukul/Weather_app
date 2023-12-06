from typing import Optional

from sqlalchemy import select, update, extract, func, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import NoResultFound

from infrastructure.database.models import User
from infrastructure.database.repo.base import BaseRepo
from datetime import date



class UserRepo(BaseRepo):
    async def get_or_create_user(
            self,
            user_id: int,
            full_name: str,
            chat_id: int,
            language: str,
            username: Optional[str] = None,


    ):
        """
        Creates or updates a new user in the database and returns the user object.

        :param user_id: The user's ID.
        :param full_name: The user's full name.
        :param language: The user's language.
        :param username: The user's username. It's an optional parameter.
        :param chat_id: The user`s chat_id
        :return: User object, None if there was an error while making a transaction.
        """

        insert_stmt = (
            insert(User)
            .values(
                user_id=user_id,
                username=username,
                full_name=full_name,
                chat_id=chat_id,
                language=language,

            )
            .on_conflict_do_update(
                index_elements=[User.user_id],
                set_=dict(
                    username=username,
                    full_name=full_name,

                ),
            )
            .returning(User)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()

    async def get_user_language(self, user_id: int) -> str:
        statement = select(User.language).where(User.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar()

    async def get_user_lang_selected(self, user_id: int) -> bool:
        statement = select(User.lang_selected).where(User.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar()

    async def change_lang_selected(self, user_id: int, lang_selected: bool) -> None:
        statement = update(User).values(lang_selected=lang_selected).where(User.user_id == user_id)
        await self.session.execute(statement)
        await self.session.commit()

    async def get_all_chat_ids(self):
        """
        Returns all chat_ids from the User table.

        :return: A list of chat_ids.
        """
        statement = select(User.chat_id)
        result = await self.session.execute(statement)
        return [row[0] for row in result.fetchall()]

    async def get_all_users(self):
        """
        Returns all users from the User table.

        :return: A list of User objects.
        """
        statement = select(User)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int):
        """
        Returns a user from the User table by ID.

        :param user_id: The user's ID.
        :return: User object, None if there was an error while making a transaction.
        """
        try:
            statement = select(User).where(User.user_id == user_id)
            result = await self.session.execute(statement)
            return result.scalar_one()
        except NoResultFound:
            return None

    async def get_users_by_date(self, today_date: date):
        """
        Returns all users from the User table that were created on the specified date.

        :param today_date: Today date
        :return: A list of User objects.
        """
        statement = select(User).where(func.date(User.created_at) == today_date)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_users_by_24h(self):
        """
        Returns all users from the User table that were created in the last 24 hours.

        :return: A list of User objects.
        """
        twenty_four_hours_ago = func.now() - text("interval '24 hours'")
        statement = select(User).where(User.created_at >= twenty_four_hours_ago)
        result = await self.session.execute(statement)
        return result.scalars().all()