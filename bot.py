from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import (
    State,
    StatesGroup
)
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

TOKEN = "8677937283:AAFVFqWZoZ2pZuIX9TKWl8eZbvsSUdaLeqg"

# ТВОЙ TELEGRAM ID
ADMIN_ID = 7088252933

# USERNAME ЗАКРЫТОГО КАНАЛА
PRIVATE_CHANNEL = -1003924101643

USDT_ADDRESS = "TTkHtaipHpPVFYUaJ2BbVs7RxBvss7LfFr"

bot = Bot(token=TOKEN)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

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
# КНОПКИ
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
# FSM
# =========================

class PaymentState(StatesGroup):

    waiting_screenshot = State()
    waiting_link = State()

# =========================
# ХРАНЕНИЕ ЗАЯВОК
# =========================

admin_requests = {}

# =========================
# СТАРТ
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
    Text(startswith="pay_")
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
        f"Оплата — {data['price']}\n\n"

        f"1. Перейдите по ссылке:\n"
        f"{data['link']}\n\n"

        f"2. Вставьте USDT TRC20 адрес:\n\n"
        f"{USDT_ADDRESS}\n\n"

        f"3. После оплаты нажмите:\n"
        f"Я оплатил"
    )

    paid_kb = InlineKeyboardMarkup()

    paid_kb.add(
        InlineKeyboardButton(
            text="✅ Я оплатил",
            callback_data="paid"
        )
    )

    await bot.send_message(
        callback.from_user.id,
        text,
        reply_markup=paid_kb
    )

    await callback.answer()

# =========================
# Я ОПЛАТИЛ
# =========================

@dp.callback_query_handler(
    lambda c: c.data == "paid"
)
async def paid(
    callback: types.CallbackQuery
):

    await PaymentState.waiting_screenshot.set()

    await bot.send_message(
        callback.from_user.id,
        "📸 Отправьте скриншот оплаты"
    )

    await callback.answer()

# =========================
# ПОЛУЧАЕМ СКРИН
# =========================

@dp.message_handler(
    content_types=types.ContentType.PHOTO,
    state=PaymentState.waiting_screenshot
)
async def get_screenshot(
    message: types.Message,
    state: FSMContext
):

    photo_id = message.photo[-1].file_id

    await state.update_data(
        screenshot=photo_id
    )

    await PaymentState.next()

    await message.answer(
        "🔗 Теперь отправьте ссылку "
        "или номер заявки"
    )

# =========================
# ПОЛУЧАЕМ ЗАЯВКУ
# =========================

@dp.message_handler(
    state=PaymentState.waiting_link
)
async def get_link(
    message: types.Message,
    state: FSMContext
):

    data = await state.get_data()

    screenshot = data["screenshot"]

    username = message.from_user.username
    user_id = message.from_user.id

    admin_message = await bot.send_message(
        ADMIN_ID,
        f"""
🔥 НОВАЯ ОПЛАТА

Username: @{username}
User ID: {user_id}

Заявка:
{message.text}

Reply командой:

/ok
/wait
/fail
"""
    )

    admin_requests[
        admin_message.message_id
    ] = user_id

    await bot.send_photo(
        ADMIN_ID,
        screenshot,
        caption="📸 Скрин оплаты"
    )

    await message.answer(
        "✅ Заявка отправлена "
        "на проверку"
    )

    await state.finish()

# =========================
# OK
# =========================

@dp.message_handler(commands=["ok"])
async def approve(message: types.Message):

    if not message.reply_to_message:
        return

    user_id = admin_requests.get(
        message.reply_to_message.message_id
    )

    if not user_id:
        return

    invite = await bot.create_chat_invite_link(
        chat_id=PRIVATE_CHANNEL,
        member_limit=1
    )

    await bot.send_message(
        user_id,
        f"✅ Оплата подтверждена\n\n"
        f"Вот ваш доступ:\n"
        f"{invite.invite_link}"
    )

    await message.reply(
        "✅ Доступ выдан"
    )

# =========================
# WAIT
# =========================

@dp.message_handler(commands=["wait"])
async def wait(message: types.Message):

    if not message.reply_to_message:
        return

    user_id = admin_requests.get(
        message.reply_to_message.message_id
    )

    if not user_id:
        return

    await bot.send_message(
        user_id,
        "⏳ Проверяем оплату"
    )

    await message.reply(
        "✅ Сообщение отправлено"
    )

# =========================
# FAIL
# =========================

@dp.message_handler(commands=["fail"])
async def fail(message: types.Message):

    if not message.reply_to_message:
        return

    user_id = admin_requests.get(
        message.reply_to_message.message_id
    )

    if not user_id:
        return

    await bot.send_message(
        user_id,
        "❌ Перевод пока не найден"
    )

    await message.reply(
        "✅ Сообщение отправлено"
    )

# =========================
# START BOT
# =========================

if __name__ == "__main__":
    executor.start_polling(dp)