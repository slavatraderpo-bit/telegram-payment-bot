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

    # =========================
    # USDT
    # =========================

    if currency == "₮ USDT":

        text = (
            f"💰 Оплата — {data['price']}\n\n"

            f"Скопируйте TRC20 адрес ниже:\n\n"

            f"`{USDT_ADDRESS}`\n\n"

            f"После оплаты дождитесь инструкции ниже."
        )

        usdt_kb = InlineKeyboardMarkup(row_width=1)

        usdt_kb.add(
            InlineKeyboardButton(
                text="📋 Скопировать адрес",
                switch_inline_query_current_chat=USDT_ADDRESS
            )
        )

        await bot.send_message(
            callback.from_user.id,
            text,
            parse_mode="Markdown",
            reply_markup=usdt_kb
        )

    # =========================
    # ДРУГИЕ ВАЛЮТЫ
    # =========================

    else:

        text = (
            f"💰 Оплата — {data['price']}\n\n"

            f"1. Скопируйте TRC20 адрес:\n\n"

            f"`{USDT_ADDRESS}`\n\n"

            f"2. Нажмите кнопку оплаты ниже."
        )

        pay_kb = InlineKeyboardMarkup(row_width=1)

        pay_kb.add(
            InlineKeyboardButton(
                text="📋 Скопировать адрес",
                switch_inline_query_current_chat=USDT_ADDRESS
            )
        )

        pay_kb.add(
            InlineKeyboardButton(
                text="💳 Оплатить",
                callback_data=f"openpay_{currency}"
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
# ИНСТРУКЦИЯ ПОСЛЕ КНОПКИ ОПЛАТЫ
# =========================
    # =========================

    support_text = (
        "📸 После оплаты отправьте:\n\n"

        "• скриншот оплаты\n"
        "• ссылку или номер заявки\n\n"

        "Менеджер проверит оплату "
        "и отправит доступ."
    )

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
# КНОПКА ОПЛАТЫ
# =========================

@dp.callback_query_handler(
    lambda c: c.data.startswith("openpay_")
)
async def open_payment(callback: types.CallbackQuery):

    currency = callback.data.replace(
        "openpay_",
        ""
    )

    data = PAYMENTS[currency]

    # Открываем ссылку оплаты
    await bot.send_message(
        callback.from_user.id,
        f"💳 Ссылка для оплаты:{data['link']}"
    )

    await callback.answer()

    # Ждем 10 секунд
    await asyncio.sleep(10)

    support_text = (
        "📸 После оплаты отправьте:"

        "• скриншот оплаты"
        "• ссылку или номер заявки"

        "Менеджер проверит оплату "
        "и отправит доступ."
    )

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