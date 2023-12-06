import operator
from operator import itemgetter

from aiogram.enums import ParseMode, ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.common.scroll import sync_scroll
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Multiselect, Column, Select, Row, NumberedPager, SwitchTo, Back
from aiogram_dialog.widgets.text import Format, ScrollingText, Const, List

from tgbot.dialogs.getters import contracts_getter, confirm_add_getter, confirm_delete_getter
from tgbot.dialogs.setters import more_info_setter, add_delete, to_name, to_description, to_confirm_add, \
    contracts_saver, contracts_deleter
from tgbot.misc import states


ID_LIST_SCROLL = "list_scroll"
ID_SYNC_SCROLL = "sync_scroll"
SCROLLS_MAIN_MENU_BUTTON = SwitchTo(
    text=Const("Back"), id="back", state=states.Scrolls.MAIN,
)




def main_window():
    return [
        Window(
            List(
                Format("{item[0]}"),
                items="title",
                id=ID_LIST_SCROLL,
                page_size=1,
            ),
            ScrollingGroup(
                Select(
                    Format("{item[0]}"),
                    id="info",
                    item_id_getter=itemgetter(1),
                    items="more_info",
                    on_click=more_info_setter,

                ),
                width=1,
                height=1,
                id=ID_SYNC_SCROLL,
                on_page_changed=sync_scroll(ID_LIST_SCROLL)
            ),
            Row(
                Select(
                    Format("{item[0]}"),
                    id="control",
                    item_id_getter=itemgetter(1),
                    items="control_buttons",
                    on_click=add_delete,

                ),
            ),
            state=states.Scrolls.SYNC,
            getter=contracts_getter,
            preview_data=contracts_getter,
        ),
        Window(
            Const('Please add address:'),
            MessageInput(to_name, ContentType.TEXT),
            parse_mode=ParseMode.HTML,
            state=states.Scrolls.address,
        ),
        Window(
            Const('Please add name:'),
            MessageInput(to_description, ContentType.TEXT),
            parse_mode=ParseMode.HTML,
            state=states.Scrolls.name,
        ),
        Window(
            Const('Please add description:'),
            MessageInput(to_confirm_add, ContentType.TEXT),
            parse_mode=ParseMode.HTML,
            state=states.Scrolls.description,
        ),
        Window(
            Format('{title}'),
            Column(
                Select(
                    Format("{item[0]}"),
                    id="confirm_add",
                    item_id_getter=operator.itemgetter(1),
                    items="control_buttons",
                    on_click=contracts_saver,
                ),
            ),
            parse_mode=ParseMode.HTML,
            state=states.Scrolls.confirm_add,
            getter=confirm_add_getter,
        ),
        Window(
            Format('{title}'),
            Column(
                Select(
                    Format("{item[0]}"),
                    id="confirm_delete",
                    item_id_getter=operator.itemgetter(1),
                    items="control_buttons",
                    on_click=contracts_deleter,
                ),
                SwitchTo(
                    text=Const("Back"), id="back", state=states.Scrolls.SYNC,
                )
            ),
            parse_mode=ParseMode.HTML,
            state=states.Scrolls.confirm_delete,
            getter=confirm_delete_getter,
        ),

    ]

