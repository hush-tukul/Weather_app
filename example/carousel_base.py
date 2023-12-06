from __future__ import annotations

import abc
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


class CarouselBase(abc.ABC):
    """
    How to use:

    1) Initial send

    carousel = FactsCarousel(...)
    await carousel.send(update, context)

    2) On click

    carousel = FactsCarousel(...)
    await carousel.click(update, context)

    """

    ADD_BUTTON = None
    DELETE_BUTTON = True
    INLINE_QUERY_PREFIX = None
    NO_DOCUMENTS_MESSAGE = None

    def __init__(
            self,
            send_message_to_chat_id,
    ):
        self.index = 0
        self.documents = []
        self.send_message_to_chat_id = send_message_to_chat_id

    @abc.abstractmethod
    async def get_documents(self):
        pass

    async def send(self, update: Update, _: CallbackContext) -> None:
        self.index = 0
        self.documents = await self.get_documents()
        msg, reply_markup = self.get_content()
        logging.info(f'{self.__class__.__name__}: send {msg=}')
        await self.send_message_to_chat_id(
            chat_id=update.effective_chat.id, text=msg, reply_markup=reply_markup)

    @abc.abstractmethod
    def doc_to_key(self, doc):
        pass

    def get_content(self):
        if len(self.documents) == 0:
            return self.NO_DOCUMENTS_MESSAGE, None
        else:
            self.index = self.index % len(self.documents)
            doc = self.documents[self.index]
            key = self.doc_to_key(doc)
            keyboard = [
                [
                    InlineKeyboardButton("⬅️", callback_data=f'{self.INLINE_QUERY_PREFIX}:left____{self.index}'),
                ] + ([
                    InlineKeyboardButton(
                        "🆕 Add",
                             callback_data=f'{self.INLINE_QUERY_PREFIX}:add'
                    ),
                ] if self.ADD_BUTTON else []
                ) + ([
                    InlineKeyboardButton(
                        "🔥 Delete",
                             callback_data=f'{self.INLINE_QUERY_PREFIX}:delete____{self.index}____{key}'
                    ),
                ] if self.DELETE_BUTTON else []
                ) + [
                    InlineKeyboardButton("➡️", callback_data=f'{self.INLINE_QUERY_PREFIX}:right____{self.index}'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            return self.doc2str(doc), reply_markup

    @abc.abstractmethod
    def doc2str(self, doc):
        pass

    @abc.abstractmethod
    def delete(self, key):
        pass

    async def add(self, update: Update, _: CallbackContext) -> None:
        pass

    async def click(self, update: Update, _: CallbackContext) -> None:
        self.documents = await self.get_documents()

        query = update.callback_query.data
        assert query.startswith(f'{self.INLINE_QUERY_PREFIX}:')
        query = query[len(f'{self.INLINE_QUERY_PREFIX}:'):]
        logging.info(f'{self.__class__.__name__}: click query={query}')
        parts = query.split('____')
        command = parts[0]
        index = int(parts[1]) if len(parts) > 1 else None
        if command == 'left':
            assert index is not None
            if len(self.documents) > 0:
                self.index = index - 1 % len(self.documents)
            else:
                self.index = 0
        elif command == 'right':
            assert index is not None
            if len(self.documents) > 0:
                self.index = index + 1 % len(self.documents)
            else:
                self.index = 0
        elif command == 'delete':
            assert index is not None
            assert len(parts) > 2
            rest = '____'.join(parts[2:])
            key = rest
            logging.info(f'{self.__class__.__name__}: delete key={key}')
            await self.delete(key)
            self.documents = await self.get_documents()

            if len(self.documents) > 0:
                self.index = index % len(self.documents)
            else:
                self.index = 0
        elif command == 'add':
            await self.add(update, _)
        else:
            raise Exception(f'Unknown command: {command}')

        text, markup = self.get_content()
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=markup,
        )
