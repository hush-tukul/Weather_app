from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder




async def main_keyboard():
  builder = ReplyKeyboardBuilder()
  items = [
      ["🛒 Рассчитать доставку"],
      ["💴 Курс Юаня", "🔍 Поиск товара"],
      ["🌐 Сайты для поиска товаров", "⬅️ О нас"],
      ["🗣️ Задать вопрос"],
  ]
  for item in items:
      builder.add(*[KeyboardButton(text=text) for text in item])
  builder.adjust(1, 2, 2, 1)

  return builder.as_markup(
      resize_keyboard=True,
      one_time_keyboard=True,

  )


async def item_type_keyboard():
   builder = ReplyKeyboardBuilder()
   items = [
       ["Одежда", "Сумки"],
       ["Обувь", "Ремни"],
       ["Мебель", "Автозапчасти"],
       ["Электроника", "Игрушки"],
       ["Косметика", "Хоз.товары"],
       ["Другое"]
   ]
   for item in items:
       builder.add(*[KeyboardButton(text=text) for text in item])
   builder.adjust(2, 2, 2, 2, 2, 1)
   return builder.as_markup(
       resize_keyboard=True,
       one_time_keyboard=True,
   )