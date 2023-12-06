import logging

from aiogram import Router


from tgbot.filters.admin import AdminFilter


logger = logging.getLogger(__name__)

admin_router = Router()
admin_router.message.filter(AdminFilter())


