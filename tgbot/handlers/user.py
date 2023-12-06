import logging

from aiogram import Router, F
from aiogram.enums import ContentType, ChatType
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, StartMode

from infrastructure.database.repo.requests import RequestsRepo
from tgbot.keyboards.reply import main_keyboard, item_type_keyboard
from tgbot.misc import states

logger = logging.getLogger(__name__)

user_router = Router()


@user_router.message(CommandStart())
async def gate_start(m: Message, repo: RequestsRepo, dialog_manager: DialogManager):
    logger.info(f"You are in gate_start")
    user_data = dialog_manager.middleware_data.get("user")
    logger.info(f"user_data: {user_data.user_id}")
    await m.answer("Hi, welcome to Test_bot. Please provide /set_contracts command to try what it can.")


@user_router.message(Command("set_contracts"))
async def main_menu(m: Message, repo: RequestsRepo, dialog_manager: DialogManager):
    logger.info(f"You are in gate_start")
    user_data = dialog_manager.middleware_data.get("user")
    logger.info(f"user_data: {user_data.user_id}")
    await dialog_manager.start(states.Scrolls.SYNC, mode=StartMode.RESET_STACK)



