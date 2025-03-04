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
    "kk": "\ud83c\udde6\ud83c\uddff Қазақша",
    "ru": "\ud83c\uddf7\ud83c\uddfa Русский",
    "en": "\ud83c\uddec\ud83c\udde7 English"
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
        [KeyboardButton(text=LANGUAGES["kk"])],
        [KeyboardButton(text=LANGUAGES["ru"])],
        [KeyboardButton(text=LANGUAGES["en"])],
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
                text=MESSAGES[lang]["orders"]
            )],
            [KeyboardButton(text="🌍 Тілді өзгерту / Сменить язык / Change Language")]
        ],
        resize_keyboard=True
    )

    await message.answer(MESSAGES[lang]["start"], reply_markup=keyboard)

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
