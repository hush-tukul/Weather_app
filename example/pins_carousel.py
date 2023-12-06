from __future__ import annotations

import json
import logging
import datetime

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from db import Config, PinnedMessage
from menus.carousel_base import CarouselBase
from semantic_service.semantic_client import SemanticDBClient


class PinsCarousel(CarouselBase):
    INLINE_QUERY_PREFIX = 'pins'
    NO_DOCUMENTS_MESSAGE = 'No facts in the Pins database.\n\nUse `/pin`'

    ADD_BUTTON = True

    def __init__(
            self,
            config: Config,
            chat_id: str | int | None,
            send_message_to_chat_id,
            semantic_db_client: SemanticDBClient,
    ):
        super().__init__(
            send_message_to_chat_id=send_message_to_chat_id,
        )
        self.semantic_db_client = semantic_db_client
        self.config = config
        self.chat_id = chat_id

    async def get_documents(self) -> list[PinnedMessage]:
        response = self.config.get_all_pinned_messages(chat_id=self.chat_id)
        return response

    def doc_to_key(self, doc: PinnedMessage):
        return doc['message_id']

    def doc2str(self, doc: PinnedMessage):
        if doc['timestamp']:
            _dt = datetime.datetime.fromtimestamp(doc['timestamp']).date().strftime("%Y-%m-%d")
        else:
            _dt = 'unknown'

        if doc['from_user']['username']:
            _from = '@' + doc['from_user']['username']
        else:
            _from = doc['from_user']['full_name']

        return f'''Pinned ({self.index + 1}/{len(self.documents)}):

From: {_from}
Date: {_dt}
Message:
{doc['text']}
'''.strip()

    async def delete(self, key):
        logging.info(f'{self.__class__.__name__}: delete {key=}')
        self.config.remove_pinned_message(chat_id=self.chat_id, message_id=key)
        scope_id = self.config.get_chat_scope_id(chat_id=self.chat_id)
        if not scope_id:
            raise Exception(f'No scope_id for chat_id={self.chat_id}')
        helpers = await self.semantic_db_client.get(
            scope_id=scope_id,
        )
        for helper in helpers.documents:
            metadata = helper.metadata
            if not metadata:
                logging.info(f'{self.__class__.__name__}: no metadata {helper.id=}')
                continue
            pin_message = metadata.get('pin_message')
            if not pin_message:
                logging.info(f'{self.__class__.__name__}: no pin_message {helper.id=}, {metadata=}')
                continue
            pin_message = json.loads(pin_message)
            if str(pin_message['message_id']) == str(key):
                logging.info(f'{self.__class__.__name__}: SEMANTIC delete {helper.id=}')
                await self.semantic_db_client.delete(
                    scope_id=scope_id,
                    ids=[helper.id],
                )
            else:
                logging.info(f'{self.__class__.__name__}: SEMANTIC keep {helper.id=}, {pin_message=}')
        self.documents = await self.get_documents()

    async def add(self, update, context):
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        self.config.set_last_chat_user_command(
            chat_id=chat_id,
            user_id=user_id,
            command='pin',
        )
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                '✖️ Cancel',
                callback_data=f'cancel-pin:{chat_id}:{user_id}',
            )],
        ])
        await self.send_message_to_chat_id(
            chat_id=update.effective_chat.id,
            text='Forward a historical message to this chat, I will remember it as pinned.',
            reply_markup=reply_markup
        )
