import logging
import asyncio
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import requests

TOKEN = "7656620027:AAFMvmxiOqelHS3hC2IwsaWthlAg3DxRPmA"
ADMIN_ID = 123456789

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_languages = {}

LANGUAGES = {
    "kk": "🇰🇿 Қазақша",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English"
}

MESSAGES = {
    "kk": {
        "start": "Сәлем! 🌸\nBlooooom ботына қош келдіңіз.\nБұл бот гүлге жазылуға көмектеседі.\n\nТөмендегі мәзірден таңдаңыз ⬇️",
        "orders": "📦 Менің тапсырыстарым",
        "no_orders": "Сізде әлі тапсырыстар жоқ.",
        "about": "Blooooom — гүлге жазылу қызметі, ол сізге қуаныш пен әсемдік сыйлайды! 🌺",
        "contacts": "Бізбен байланыс:\n📧 Email: staff@blooooom.kz\n📱 Telegram: @oljawave\n📞 Телефон: +7 (708) 517-64-91",
        "choose_lang": "Тілді таңдаңыз:",
        "lang_set": "✅ Тіл орнатылды: Қазақша"
    },
    "ru": {
        "start": "Привет! 🌸\nДобро пожаловать в Blooooom.\nЭтот бот поможет вам оформить подписку на цветы.\n\nВыберите действие из меню ниже ⬇️",
        "orders": "📦 Мои заказы",
        "no_orders": "У вас пока нет заказов.",
        "about": "Blooooom — это сервис подписки на цветы, который приносит радость и красоту прямо к вам домой! 🌺",
        "contacts": "Связаться с нами можно через:\n📧 Email: staff@blooooom.kz\n📱 Telegram: @oljawave\n📞 Телефон: +7 (708) 517-64-91",
        "choose_lang": "Выберите язык:",
        "lang_set": "✅ Язык установлен: Русский"
    },
    "en": {
        "start": "Hello! 🌸\nWelcome to Blooooom.\nThis bot will help you subscribe to flowers.\n\nChoose an action from the menu below ⬇️",
        "orders": "📦 My Orders",
        "no_orders": "You don't have any orders yet.",
        "about": "Blooooom is a flower subscription service that brings joy and beauty directly to your home! 🌺",
        "contacts": "You can contact us via:\n📧 Email: staff@blooooom.kz\n📱 Telegram: @oljawave\n📞 Phone: +7 (708) 517-64-91",
        "choose_lang": "Choose a language:",
        "lang_set": "✅ Language set: English"
    }
}

# Клавиатура для выбора языка
language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(LANGUAGES["kk"])],
        [KeyboardButton(LANGUAGES["ru"])],
        [KeyboardButton(LANGUAGES["en"])]
    ],
    resize_keyboard=True
)


@dp.message(F.text == "/start")
async def start_handler(message: Message):
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "kk")  

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="💐 Жазылу рәсімдеу" if lang == "kk" else "💐 Оформить подписку" if lang == "ru" else "💐 Subscribe",
                web_app=WebAppInfo(url=f"https://oljawave.github.io/bloom-tg-miniapp/?user_id={user_id}")
            )],
            [KeyboardButton(text=MESSAGES[lang]["orders"])],
            [KeyboardButton(text="ℹ️ Біздің жайлы" if lang == "kk" else "ℹ️ О нас" if lang == "ru" else "ℹ️ About us")],
            [KeyboardButton(text="📞 Байланыс" if lang == "kk" else "📞 Контакты" if lang == "ru" else "📞 Contact us")],
            [KeyboardButton(text="🌍 Тілді өзгерту / Сменить язык / Change Language")]
        ],
        resize_keyboard=True
    )

    await message.answer(MESSAGES[lang]["start"], reply_markup=keyboard)

@dp.message(F.text == "📦 Менің тапсырыстарым")
@dp.message(F.text == "📦 Мои заказы")
@dp.message(F.text == "📦 My Orders")
async def my_orders(message: types.Message):
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "kk")

    response = requests.get(f"https://bloom-backend-production.up.railway.app/orders/{user_id}")

    if response.status_code == 200:
        orders = response.json().get("orders", [])

        if not orders:
            await message.answer(MESSAGES[lang]["no_orders"])
            return
        
        text = "Сіздің тапсырыстарыңыз:\n\n" if lang == "kk" else "Ваши заказы:\n\n" if lang == "ru" else "Your Orders:\n\n"
        for order in orders:
            dates = ', '.join(order['dates'])
            text += (
                f"📌 <b>Тапсырыс #{order['order_id']}</b>\n"
                f"📅 <b>Күні:</b> {dates}\n"
                f"💰 <b>Бюджет:</b> {order['price_range']}\n"
                f"📍 <b>Мекен-жайы:</b> {order['address']}\n"
                f"📞 <b>Телефон:</b> {order['phone']}\n\n"
            )

        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer(MESSAGES[lang]["no_orders"])

@dp.message(F.text == "ℹ️ Біздің жайлы")
@dp.message(F.text == "ℹ️ О нас")
@dp.message(F.text == "ℹ️ About us")
async def about_handler(message: Message):
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "kk")
    await message.answer(MESSAGES[lang]["about"])

@dp.message(F.text == "📞 Байланыс")
@dp.message(F.text == "📞 Контакты")
@dp.message(F.text == "📞 Contact us")
async def contacts_handler(message: Message):
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "kk")
    await message.answer(MESSAGES[lang]["contacts"])

# 🌍 Выбор языка
@dp.message(F.text == "🌍 Тілді өзгерту / Сменить язык / Change Language")
async def change_language(message: Message):
    await message.answer(MESSAGES["kk"]["choose_lang"], reply_markup=language_keyboard)

@dp.message(lambda message: message.text in LANGUAGES.values())
async def set_language(message: Message):
    user_id = message.from_user.id
    lang = next(key for key, value in LANGUAGES.items() if value == message.text)
    user_languages[user_id] = lang  

    await message.answer(MESSAGES[lang]["lang_set"])
    await start_handler(message)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
