from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from aiogram.utils import executor
import asyncio

TOKEN = "8677937283:AAFVFqWZoZ2pZuIX9TKWl8eZbvsSUdaLeqg"

# ТВОЙ USERNAME БЕЗ @
ADMIN_USERNAME = "keysiboss"

USDT_ADDRESS = "TTkHtaipHpPVFYUaJ2BbVs7RxBvss7LfFr"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

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

    await message.answer(
        "💰 Чем будешь платить?",
        reply_markup=payment_kb
    )

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

    support_kb = InlineKeyboardMarkup()

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

    await bot.send_message(
        callback.from_user.id,
        support_text,
        reply_markup=support_kb
    )

# =========================
# START BOT
# =========================

if __name__ == "__main__":
    executor.start_polling(dp)