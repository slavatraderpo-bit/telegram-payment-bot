from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.utils import executor

TOKEN = "8677937283:AAFVFqWZoZ2pZuIX9TKWl8eZbvsSUdaLeqg"

ADMIN_ID = 7088252933

CHANNEL_LINK = "https://t.me/+iLSq7JqsJoBmYjc0"

USDT_ADDRESS = "TTkHtaipHpPVFYUaJ2BbVs7RxBvss7LfFr"

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

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

menu = ReplyKeyboardMarkup(
    resize_keyboard=True
)

for key in PAYMENTS.keys():
    menu.add(KeyboardButton(key))

menu.add(
    KeyboardButton("Я оплатил")
)

waiting_users = {}

@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    await message.answer(
        "Выберите валюту оплаты:",
        reply_markup=menu
    )

@dp.message_handler(lambda message: message.text in PAYMENTS)
async def payment_method(message: types.Message):

    data = PAYMENTS[message.text]

    text = (
        f"Оплата — {data['price']}\n\n"
        f"1. Перейдите по ссылке:\n"
        f"{data['link']}\n\n"
        f"2. Вставьте USDT TRC20 адрес:\n\n"
        f"{USDT_ADDRESS}\n\n"
        f"3. После оплаты нажмите:\n"
        f"Я оплатил"
    )

    await message.answer(text)

@dp.message_handler(
    lambda message: message.text == "Я оплатил"
)
async def paid(message: types.Message):

    waiting_users[message.from_user.id] = True

    await message.answer(
        "Отправьте:\n"
        "- скрин оплаты\n"
        "- ссылку или номер заявки"
    )

@dp.message_handler(
    content_types=types.ContentTypes.ANY
)
async def get_payment(message: types.Message):

    if message.from_user.id in waiting_users:

        username = message.from_user.username
        user_id = message.from_user.id

        text = (
            f"НОВАЯ ЗАЯВКА\n\n"
            f"Username: @{username}\n"
            f"User ID: {user_id}\n\n"
            f"Ответьте:\n"
            f"/ok\n"
            f"/wait\n"
            f"/fail"
        )

        sent = await bot.send_message(
            ADMIN_ID,
            text
        )

        if message.photo:

            await bot.send_photo(
                ADMIN_ID,
                message.photo[-1].file_id
            )

        if message.text:

            await bot.send_message(
                ADMIN_ID,
                f"Текст:\n{message.text}"
            )

        waiting_users[sent.message_id] = user_id

        await message.answer(
            "Заявка отправлена ✅"
        )

        del waiting_users[
            message.from_user.id
        ]

@dp.message_handler(commands=["ok"])
async def approve(message: types.Message):

    if message.reply_to_message:

        user_id = waiting_users.get(
            message.reply_to_message.message_id
        )

        if user_id:

            await bot.send_message(
                user_id,
                f"Оплата подтверждена ✅\n\n"
                f"Вот ссылка на канал:\n"
                f"{CHANNEL_LINK}"
            )

            await message.answer(
                "Доступ выдан ✅"
            )

@dp.message_handler(commands=["wait"])
async def wait(message: types.Message):

    if message.reply_to_message:

        user_id = waiting_users.get(
            message.reply_to_message.message_id
        )

        if user_id:

            await bot.send_message(
                user_id,
                "Проверяем оплату ⏳"
            )

            await message.answer(
                "Сообщение отправлено ✅"
            )

@dp.message_handler(commands=["fail"])
async def fail(message: types.Message):

    if message.reply_to_message:

        user_id = waiting_users.get(
            message.reply_to_message.message_id
        )

        if user_id:

            await bot.send_message(
                user_id,
                "Перевод пока не найден ❌"
            )

            await message.answer(
                "Сообщение отправлено ✅"
            )

if __name__ == "__main__":
    executor.start_polling(dp)