import datetime
import logging
from datetime import date

from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaId, MediaAttachment
from aiogram_dialog.widgets.input import MessageInput
from environs import Env

from infrastructure.database.repo.requests import RequestsRepo


logger = logging.getLogger(__name__)

env = Env()


async def product_getter(**_kwargs):
    return {
        "products": [(f"Product {i}", i) for i in range(1, 30)],
    }

async def contracts_getter(
        repo: RequestsRepo,
        dialog_manager: DialogManager,
        **kwargs,
):
    logger.info("You are in contracts_getter")
    tg_id = dialog_manager.event.from_user.id
    contracts = await repo.users_contracts.get_contracts_by_tg_id(tg_id=tg_id)
    title = [((f"Contract address: {contract.contract_name}"
              f"\n\nContract name: {contract.contract_address}"
              f"\n\nContract description: {contract.contract_description}"), contract.contract_id) for contract in contracts] if contracts else [('You have no contracts yet', "no_contract")]

    more_info = [
        ("More info", "more_info"),
    ] * len(title)
    control_buttons = [
        ('Delete', 'delete'),
        ('Add', 'add'),
    ]
    return {
        "title": title,
        "more_info": more_info,
        "control_buttons": control_buttons if title[0][1] != "no_contract" else [control_buttons[-1]]

    }


async def confirm_add_getter(
        repo: RequestsRepo,
        dialog_manager: DialogManager,
        **kwargs,
):
    logger.info("You are in confirm_add_getter")
    data = [dialog_manager.dialog_data.get(i) for i in ['address', 'name', 'description']]
    title = (
        "Your contract: "
        f"\nAddress: {data[0]}"
        f"\nName: {data[1]}"
        f"\nDescription: {data[2]}"

    )
    control_buttons = [
        ("✅Confirm", "confirm"),
        ("Cancel", "cancel")
    ]
    return {
        "title": title,
        "control_buttons": control_buttons,
    }

async def confirm_delete_getter(
        repo: RequestsRepo,
        dialog_manager: DialogManager,
        **kwargs,
):
    logger.info("You are in confirm_delete_getter")
    current_contract = dialog_manager.dialog_data.get("current_contract_id")
    contract_data = await repo.users_contracts.get_contracts_by_contract_id(contract_id=current_contract)
    title = (
        "Your contract: "
        f"\nAddress: {contract_data[0].contract_address}"
        f"\nName: {contract_data[0].contract_name}"
        f"\nDescription: {contract_data[0].contract_description}"

    )
    control_buttons = [
        ("🚫Delete", "delete")
    ]
    return {
        "title": title,
        "control_buttons": control_buttons,
    }