from __future__ import annotations

import logging

from menus.carousel_base import CarouselBase
from semantic_service.semantic_client import SemanticDBClient
from semantic_service.types import SemanticDocument


class MemsCarousel(CarouselBase):
    INLINE_QUERY_PREFIX = 'mems'
    NO_DOCUMENTS_MESSAGE = 'No facts in the Knowledge base.\n\nUse `/mem Question: The meaning of life? Answer: 42`'

    def __init__(
            self,
            scope_id: str | None,
            send_message_to_chat_id,
            semantic_db_client: SemanticDBClient,
    ):
        super().__init__(
            send_message_to_chat_id=send_message_to_chat_id,
        )
        self.semantic_db_client = semantic_db_client
        self.scope_id = scope_id

    async def get_documents(self):
        response = await self.semantic_db_client.get_mems(scope_id=self.scope_id)
        return response.documents

    async def add(self, update, context):
        await self.send_message_to_chat_id(
            chat_id=update.effective_chat.id,
            text='Use /mem command to add a new fact.',
        )

    def doc_to_key(self, doc):
        return doc.id

    def doc2str(self, doc: SemanticDocument):
        return f'''Fact ({self.index + 1}/{len(self.documents)}):

{doc.chunk}'''

    async def delete(self, key):
        await self.semantic_db_client.delete(
            scope_id=self.scope_id,
            ids=[key],
        )
        self.documents = await self.get_documents()
