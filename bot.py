from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils import executor

TOKEN = "8677937283:AAFVFqWZoZ2pZuIX9TKWl8eZbvsSUdaLeqg"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ID STORAGE КАНАЛА
STORAGE_CHAT_ID = -1003924101643

# ID СООБЩЕНИЯ С ВИДЕО
VIDEO_MESSAGE_ID = 2

# КНОПКА
start_kb = InlineKeyboardMarkup()

start_kb.add(
    InlineKeyboardButton(
        text="🔥 Забрать первое видео",
        callback_data="video1"
    )
)

# START
@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    text = (
        "🔥 Привет! Ты в системе.\n\n"

        "Я записал для тебя 3 коротких видео — "
        "в них вся суть метода faceless-блогинга "
        "через AI-персонажей.\n\n"

        "▸ Видео 1: Как выбрать тему для блога\n"
        "▸ Видео 2: 2 формата контента и какие нейросети использовать\n"
        "▸ Видео 3: Как монетизировать свой блог\n\n"

        "Каждое — 1.5-2 минуты. Без воды.\n\n"

        "Готов? Жми кнопку — открою первое 👇\n\n"

        "⚠️ ВНИМАНИЕ:\n"
        "ЭТИ ВИДЕО БУДУТ УДАЛЕНЫ ЧЕРЕЗ 48 ЧАСОВ"
    )

    await message.answer(
        text,
        reply_markup=start_kb
    )

# КНОПКА ВИДЕО
@dp.callback_query_handler(
    lambda c: c.data == "video1"
)
async def send_video(callback: types.CallbackQuery):

    await bot.copy_message(
        chat_id=callback.from_user.id,
        from_chat_id=STORAGE_CHAT_ID,
        message_id=VIDEO_MESSAGE_ID
    )

    await callback.answer()

if __name__ == "__main__":
    executor.start_polling(dp)