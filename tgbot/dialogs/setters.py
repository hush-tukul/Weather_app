import asyncio
import logging
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from infrastructure.database.repo.requests import RequestsRepo
from tgbot.misc.states import Scrolls

logger = logging.getLogger(__name__)


async def add_delete(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        control_button: str
):
    logger.info("You are in contracts_switcher")
    logger.info(f"control_button: {control_button}")
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")
    tg_id = dialog_manager.event.from_user.id
    contracts = await repo.users_contracts.get_contracts_by_tg_id(tg_id=tg_id)
    data = dialog_manager.find('list_scroll')
    current_page = await data.get_page()
    if contracts:
        logger.info(
            f"add_delete current_page {contracts[current_page].contract_id}")

        dialog_manager.dialog_data.update(
            current_contract_id=contracts[current_page].contract_id)
        g = {
            "delete": Scrolls.confirm_delete,
            "add": Scrolls.address,
        }
        await dialog_manager.switch_to(g[control_button])
    else:
        g = {
            "delete": Scrolls.confirm_delete,
            "add": Scrolls.address,
        }
        await dialog_manager.switch_to(g[control_button])


async def to_name(m: Message, widget: MessageInput,
                         dialog_manager: DialogManager):
    logger.info("You are in to_name")
    logger.info(f"text provided: {m.text}")
    dialog_manager.dialog_data.update(address=m.text)
    await dialog_manager.switch_to(Scrolls.name)


async def to_description(m: Message, widget: MessageInput,
                         dialog_manager: DialogManager):
    logger.info("You are in to_description")
    logger.info(f"text provided: {m.text}")
    dialog_manager.dialog_data.update(name=m.text)
    await dialog_manager.switch_to(Scrolls.description)


async def to_confirm_add(m: Message, widget: MessageInput,
                         dialog_manager: DialogManager):
    logger.info("You are in to_confirm_add")
    logger.info(f"text provided: {m.text}")
    dialog_manager.dialog_data.update(description=m.text)
    await dialog_manager.switch_to(Scrolls.confirm_add)



async def contracts_saver(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        control_button: str
):
    logger.info("You are in contracts_saver")
    logger.info(f"control_button: {control_button}")
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")
    contract_data = [
        dialog_manager.dialog_data.get(i, []) for i in
        ['name', 'address', 'description']
    ]
    user_data = dialog_manager.event

    await repo.users_contracts.create_contract(
        tg_id=user_data.from_user.id,
        contract_name=contract_data[0],
        contract_address=contract_data[1],
        contract_description=contract_data[2],
    )
    await dialog_manager.start(Scrolls.SYNC)


async def contracts_deleter(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        control_button: str
):
    logger.info("You are in contracts_saver")
    logger.info(f"control_button: {control_button}")
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")
    tg_id = dialog_manager.event.from_user.id
    contracts = await repo.users_contracts.get_contracts_by_tg_id(tg_id=tg_id)
    data = dialog_manager.find('list_scroll')
    current_page = await data.get_page()
    logger.info(f"contracts_deleter current_page {current_page}")
    # contract_id = dialog_manager.dialog_data.get("current_contract_id")
    await repo.users_contracts.delete_contract_by_contract_id(
        contract_id=contracts[current_page].contract_id,
    )
    await callback.answer("Contract was deleted!")
    await dialog_manager.start(Scrolls.SYNC)

async def more_info_setter(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        control_button: str
):
    logger.info("You are in more_info_setter")
    logger.info(f"control_button: {control_button}")


