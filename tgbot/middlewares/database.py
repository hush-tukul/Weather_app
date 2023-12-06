from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from infrastructure.database.repo.requests import RequestsRepo


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool) -> None:
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            repo = RequestsRepo(session)
            if isinstance(event, CallbackQuery):
                # Use event.message.chat.id instead of event.chat.id
                chat_id = event.message.chat.id
            else:
                chat_id = event.chat.id
            user = await repo.users.get_or_create_user(
                event.from_user.id,
                event.from_user.full_name,
                chat_id,
                event.from_user.language_code,
                event.from_user.username,
            )

            data["session"] = session
            data["repo"] = repo
            data["user"] = user

            result = await handler(event, data)
        return result
