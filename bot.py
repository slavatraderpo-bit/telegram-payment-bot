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
            f"💰 Оплата — {data['price']}\n\n"

            f"Скопируйте TRC20 адрес ниже👇:\n\n"

            f"`{USDT_ADDRESS}`\n\n"

            f"После оплаты дождитесь инструкции ниже."
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

            f"1. Скопируй TRC20 адрес в один клик👇\n\n"

            f"`{USDT_ADDRESS}`\n\n"

            f"2. Нажми кнопку оплаты ниже и попадешь на страницу оплаты\n\n"
            f"3. Выбери отправить валюту которую выбрал и получить USDT TRC20\n\n"
            f"4. Введи сумму, данные карты, этот адрес USDT TRC20\n\n"
            f"5. Когда увидешь что оплата выполнена, то сохрани ссылку на перевод\n\n"

            f"Перепроверь сумму и адрес вывода USDT TRC20. Все легко, но иногда можно ошибиться и потерять деньги"
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
# START BOT
# =========================

if __name__ == "__main__":
    executor.start_polling(dp)