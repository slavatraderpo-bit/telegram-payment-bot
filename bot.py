from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from datetime import datetime, timedelta
from aiogram.utils import executor
import asyncio

TOKEN = "8677937283:AAFVFqWZoZ2pZuIX9TKWl8eZbvsSUdaLeqg"

# ТВОЙ USERNAME БЕЗ @
ADMIN_USERNAME = "keysiboss"

USDT_ADDRESS = "TTkHtaipHpPVFYUaJ2BbVs7RxBvss7LfFr"

PRIVATE_CHANNEL_ID = -1003972095670

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
# ОПЛАТЫ
# =========================

PAYMENTS = {
    "🇷🇺 RUB": {
        "price": "1299₽",
        "link": "https://sberbit.vip/exchange-cardrub-to-trc20/"
    },

    "🇺🇦 UAH": {
        "price": "699₴",
        "link": "https://coinfusion.one/exchange_CARDUAH_to_USDTTRC/"
    },

    "🇰🇿 KZT": {
        "price": "7999₸",
        "link": "https://metka.cc/?cur_from=CARDKZT&cur_to=USDTTRC20"
    },

    "🇺🇸 USD": {
        "price": "35$",
        "link": "https://fastchange.me/change/visamastercard_usd-itez_usdt_trc20"
    },

    "🇪🇺 EUR": {
        "price": "30€",
        "link": "https://fastchange.me/change/visamastercard_eur-itez_usdt_trc20"
    },

    "₮ USDT": {
        "price": "15 USDT",
        "link": ""
    }
}

# =========================
# КНОПКИ ВИДЕО
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
# КНОПКИ ВАЛЮТ
# =========================

payment_kb = InlineKeyboardMarkup(row_width=2)

for key in PAYMENTS.keys():

    payment_kb.insert(
        InlineKeyboardButton(
            text=key,
            callback_data=f"pay_{key}"
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
        "💰 Чем будешь платить?",
        reply_markup=payment_kb
    )

    await callback.answer()

# =========================
# ВЫБОР ВАЛЮТЫ
# =========================

@dp.callback_query_handler(
    lambda c: c.data.startswith("pay_")
)
async def payment_method(
    callback: types.CallbackQuery
):

    currency = callback.data.replace(
        "pay_",
        ""
    )

    data = PAYMENTS[currency]

    # =========================
    # USDT
    # =========================

    if currency == "₮ USDT":

        text = (
            f"💰 Переведи — {data['price']}\n\n"

            f"✅ На адрес USDT TRC-20. Скопируй его в один клик👇\n\n"

            f"`{USDT_ADDRESS}`\n\n"

            f"✅ Когда увидешь что оплата выполнена, сохрани ссылку на перевод и TXID если знаешь что это\n\n"

            f"‼️ Перепроверь сумму и адрес вывода USDT TRC20. Все легко, но иногда можно ошибиться и потерять деньги"
        )

        await bot.send_message(
            callback.from_user.id,
            text,
            parse_mode="Markdown"
        )

    # =========================
    # ДРУГИЕ ВАЛЮТЫ
    # =========================

    else:

        text = (
            f"💰 Для этой валюты нужно отправить — {data['price']}\n\n"

            f"✅ На адрес USDT TRC-20. Скопируй его в один клик👇\n\n"

            f"`{USDT_ADDRESS}`\n\n"

            f"✅ Нажми кнопку - Оплатить\n\n"
            f"✅ Когда увидешь что оплата выполнена, сохрани ссылку на перевод\n\n"

            f"‼️ Перепроверь сумму и адрес вывода USDT TRC20. Все легко, но иногда можно ошибиться и потерять деньги"
        )

        pay_kb = InlineKeyboardMarkup(row_width=1)

        pay_kb.add(
            InlineKeyboardButton(
                text="💳 Оплатить",
                url=data["link"]
            )
        )

        await bot.send_message(
            callback.from_user.id,
            text,
            parse_mode="Markdown",
            reply_markup=pay_kb
        )

    await callback.answer()

    # =========================
    # ЖДЕМ 10 СЕК
    # =========================

    await asyncio.sleep(10)

    # =========================
    # ИНСТРУКЦИЯ ПОСЛЕ ОПЛАТЫ
    # =========================

    support_text = (
        "✉️ После оплаты отправь:\n\n"

        "✅ скриншот оплаты\n"
        "✅ ссылку на перевод\n"
        "✅ TXID если крипта\n\n"

        "🤷 Сапорт проверит оплату и предоставит доступ"
    )

    support_kb = InlineKeyboardMarkup(row_width=1)

    support_kb.add(
        InlineKeyboardButton(
            text="📨 Отправить пруфы",
            url=(
                f"https://t.me/{ADMIN_USERNAME}"
                f"?text=Привет.%20Я%20перевел,%20"
                f"сейчас%20предоставлю%0A%0A"

                f"✅%20скриншот%20оплаты%0A"
                f"✅%20ссылка%20на%20перевод%0A"
                f"✅%20TXID%20если%20крипта"
            )
        )
    )

    support_kb.add(
        InlineKeyboardButton(
            text="💰 Выбрать валюту оплаты",
            callback_data="back_to_payments"
        )
    )

    await bot.send_message(
        callback.from_user.id,
        support_text,
        reply_markup=support_kb
    )

# =========================
# ВЕРНУТЬСЯ К ОПЛАТЕ
# =========================

@dp.callback_query_handler(
    lambda c: c.data == "back_to_payments"
)
async def back_to_payments(
    callback: types.CallbackQuery
):

    await guide(callback)

# =========================
# ВЫДАЧА ОДНОРАЗОВЫХ ССЫЛОК
# =========================
@dp.message_handler(commands=["link"])
async def get_link(message: types.Message):

    # Только для тебя
    if message.from_user.username != ADMIN_USERNAME:
        return

    invite = await bot.create_chat_invite_link(
        chat_id=PRIVATE_CHANNEL_ID,
        member_limit=1,
        expire_date=datetime.now() + timedelta(minutes=5)
    )

    await message.answer(
        f"🔗 Одноразовая ссылка:\n\n"
        f"{invite.invite_link}"
    )

# =========================
# КНОПКА НАПИСАТЬ САПОРТУ
# =========================

@dp.message_handler(commands=["support"])
async def support(message: types.Message):

    support_kb = InlineKeyboardMarkup()

    support_kb.add(
        InlineKeyboardButton(
            text="💬 Написать саппорту",
            url=(
                f"https://t.me/{ADMIN_USERNAME}"
                f"?text=Привет,%20"
                f"мне%20нужна%20помощь"
            )
        )
    )

    await message.answer(
        "Нашел проблему?",
        reply_markup=support_kb
    )

# =========================
# START BOT
# =========================

if __name__ == "__main__":
    executor.start_polling(dp)