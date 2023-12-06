from aiogram.fsm.state import StatesGroup, State



class Scrolls(StatesGroup):
    MAIN = State()
    DEFAULT_PAGER = State()
    PAGERS = State()
    LIST = State()
    TEXT = State()
    STUB = State()
    SYNC = State()
    address = State()
    name = State()
    description = State()
    confirm_add = State()
    confirm_delete = State()
