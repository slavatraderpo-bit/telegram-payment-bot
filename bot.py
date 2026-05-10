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
        "price": "30 USDT",
        "link": USDT_ADDRESS
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
        "💰 Выберите валюту оплаты:",
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

    text = (
        f"💰 Оплата — {data['price']}\n\n"

        f"1. Нажмите кнопку ниже:\n\n"

        f"2. Вставьте этот USDT TRC20 адрес:\n\n"
        f"{USDT_ADDRESS}"
    )

    # КНОПКА ОПЛАТЫ
    pay_kb = InlineKeyboardMarkup()

    pay_kb.add(
        InlineKeyboardButton(
            text="💳 Оплатить",
            url=data["link"]
        )
    )

    await bot.send_message(
        callback.from_user.id,
        text,
        reply_markup=pay_kb
    )

    await callback.answer()

    # ЖДЕМ 10 СЕК
    await asyncio.sleep(10)

    # ТЕКСТ ПОСЛЕ ОПЛАТЫ
    support_text = (
        "📸 После оплаты отправьте:\n\n"

        "• скриншот оплаты\n"
        "• ссылку или номер заявки\n\n"

        "Менеджер проверит оплату "
        "и отправит доступ."
    )

    # КНОПКА В ЛИЧКУ
    support_kb = InlineKeyboardMarkup()

    support_kb.add(
        InlineKeyboardButton(
            text="📨 Отправить",
            url=(
                f"https://t.me/{ADMIN_USERNAME}"
                f"?text=Вот%20моя%20оплата"
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