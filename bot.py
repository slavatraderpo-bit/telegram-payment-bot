from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils import executor
import asyncio

TOKEN = "8677937283:AAFVFqWZoZ2pZuIX9TKWl8eZbvsSUdaLeqg"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# =========================
# STORAGE CHANNEL DATA
# =========================

STORAGE_CHAT_ID = -1003924101643

VIDEO_1_ID = 2
VIDEO_2_ID = 7
VIDEO_3_ID = 8

# =========================
# КНОПКИ
# =========================

start_kb = InlineKeyboardMarkup()

start_kb.add(
    InlineKeyboardButton(
        text="🔥 Забрать первое видео",
        callback_data="video1"
    )
)

video2_kb = InlineKeyboardMarkup()

video2_kb.add(
    InlineKeyboardButton(
        text="🔥 Открыть второе видео",
        callback_data="video2"
    )
)

video3_kb = InlineKeyboardMarkup()

video3_kb.add(
    InlineKeyboardButton(
        text="🔥 Открыть третье видео",
        callback_data="video3"
    )
)

guide_kb = InlineKeyboardMarkup()

guide_kb.add(
    InlineKeyboardButton(
        text="💰 Забрать руководство за 990₽",
        callback_data="guide"
    )
)

# =========================
# START
# =========================

@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    text = (
        "🔥 Привет! Ты в системе.\n"
        "Я записал для тебя 3 коротких видео — "
        "в них вся суть метода faceless-блогинга "
        "через AI-персонажей.\n\n"

        "▸ Видео 1: Как выбрать тему для блога\n"
        "▸ Видео 2: 2 формата контента и какие нейросети использовать\n"
        "▸ Видео 3: Как монетизировать свой блог\n\n"

        "Каждое — 1.5-2 минуты. Без воды.\n"
        "Готов? Жми кнопку — открою первое 👇\n\n"

        "⚠️ ВНИМАНИЕ: "
        "ЭТИ ВИДЕО БУДУТ УДАЛЕНЫ ЧЕРЕЗ 48 ЧАСОВ"
    )

    await message.answer(
        text,
        reply_markup=start_kb
    )

# =========================
# ВИДЕО 1
# =========================

@dp.callback_query_handler(
    lambda c: c.data == "video1"
)
async def video1(callback: types.CallbackQuery):

    await bot.copy_message(
        chat_id=callback.from_user.id,
        from_chat_id=STORAGE_CHAT_ID,
        message_id=VIDEO_1_ID
    )

    await callback.answer()

    await asyncio.sleep(10)

    text2 = (
        "🔥 Красавчик, что досмотрел!\n"
        "Что ты получил:\n\n"

        "✓ Понимание двух путей выбора темы\n"
        "✓ Знание, что темы не придумываются — заимствуются\n\n"

        "Что дальше:\n"
        "🎬 Видео 2 — 2 формата контента и какие нейросети использовать.\n\n"

        "Тут начинается мясо. Жми 👇"
    )

    await bot.send_message(
        callback.from_user.id,
        text2,
        reply_markup=video2_kb
    )

# =========================
# ВИДЕО 2
# =========================

@dp.callback_query_handler(
    lambda c: c.data == "video2"
)
async def video2(callback: types.CallbackQuery):

    await bot.copy_message(
        chat_id=callback.from_user.id,
        from_chat_id=STORAGE_CHAT_ID,
        message_id=VIDEO_2_ID
    )

    await callback.answer()

    await asyncio.sleep(10)

    text3 = (
        "🚀 Топ! Ты уже знаешь больше, чем "
        "80% «начинающих faceless-блогеров».\n\n"

        "Что ты получил:\n"

        "✓ 2 рабочих формата AI-контента\n"
        "✓ Список конкретных нейросетей\n"
        "✓ Понимание, где брать темы\n\n"

        "Что дальше:\n\n"

        "🎬 Видео 3 — как я заработал 30 000₽ "
        "с 250 подписчиками AI-персонажа.\n\n"

        "Реальная формула с цифрами. Жми 👇"
    )

    await bot.send_message(
        callback.from_user.id,
        text3,
        reply_markup=video3_kb
    )

# =========================
# ВИДЕО 3
# =========================

@dp.callback_query_handler(
    lambda c: c.data == "video3"
)
async def video3(callback: types.CallbackQuery):

    await bot.copy_message(
        chat_id=callback.from_user.id,
        from_chat_id=STORAGE_CHAT_ID,
        message_id=VIDEO_3_ID
    )

    await callback.answer()

    await asyncio.sleep(10)

    final_text = (
        "🔥 Ну вот ты и в топ-10%.\n\n"

        "Ты досмотрел все 3 видео. "
        "Это значит ты не зритель — ты делатель.\n\n"

        "Что ты уже знаешь:\n"

        "✓ Как выбрать тему\n"
        "✓ Как создавать AI-персонажа и контент\n"
        "✓ Как продать первое\n\n"

        "Это база. Полная система — внутри руководства:\n\n"

        "📘 50 страниц без воды\n"
        "📘 Создание AI-персонажа A→Z "
        "(Nano Banana Pro + HeyGen)\n"
        "📘 50+ готовых хуков под разные ниши\n"
        "📘 Шаблоны для обоих форматов\n"
        "📘 Подключение оплаты "
        "(LavaTop за 15 минут)\n"
        "📘 ПРАВА НА ПЕРЕПРОДАЖУ — "
        "окупится одной продажей\n\n"

        "Сейчас 990₽ вместо 2490₽.\n\n"

        "+ Бонусом: моё обучение в записи 🎁\n\n"

        "Забрать руководство за 990₽👇"
    )

    await bot.send_message(
        callback.from_user.id,
        final_text,
        reply_markup=guide_kb
    )

# =========================
# КНОПКА РУКОВОДСТВА
# =========================

@dp.callback_query_handler(
    lambda c: c.data == "guide"
)
async def guide(callback: types.CallbackQuery):

    await bot.send_message(
        callback.from_user.id,
        "💰 Здесь позже будет оплата."
    )

    await callback.answer()

# =========================
# START BOT
# =========================

if __name__ == "__main__":
    executor.start_polling(dp)