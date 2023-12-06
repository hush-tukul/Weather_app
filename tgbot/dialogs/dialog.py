from aiogram_dialog import Dialog

from tgbot.dialogs.windows import main_window


def bot_menu_dialogs():
    return [
        Dialog(*main_window()),
    ]