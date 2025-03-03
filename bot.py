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

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    user_id = message.from_user.id

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="💐 Оформить подписку", 
                web_app=WebAppInfo(url=f"https://oljawave.github.io/bloom-tg-miniapp/?user_id={user_id}")
            )],
            [KeyboardButton(text="📦 Мои заказы")],
            [KeyboardButton(text="ℹ️ О нас")],
            [KeyboardButton(text="📞 Контакты")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Привет! 🌸\n"
        "Добро пожаловать в Blooooom.\n"
        "Этот бот поможет вам оформить подписку на цветы.\n\n"
        "Выберите действие из меню ниже ⬇️",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text == "📦 Мои заказы")
async def my_orders(message: types.Message):
    user_id = message.from_user.id  
    response = requests.get(f"https://bloom-backend-production.up.railway.app/orders/{user_id}")  

    if response.status_code == 200:
        orders = response.json().get("orders", [])

        if not orders:
            await message.answer("У вас пока нет заказов.")
            return
        
        text = "Ваши заказы:\n\n"
        for order in orders:
            dates = ', '.join(order['dates'])
            text += (
                f"📌 <b>Заказ #{order['order_id']}</b>\n"
                f"📅 <b>Даты доставки:</b> {dates}\n"
                f"💰 <b>Бюджет:</b> {order['price_range']}\n"
                f"📍 <b>Адрес:</b> {order['address']}\n"
                f"📞 <b>Телефон:</b> {order['phone']}\n\n"
            )

        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer("У вас пока нет заказов")


@dp.message(F.text == "ℹ️ О нас")
async def about_handler(message: Message):
    await message.answer("Blooooom — это сервис подписки на цветы, который приносит радость и красоту прямо к вам домой! 🌺")

@dp.message(F.text == "📞 Контакты")
async def contacts_handler(message: Message):
    await message.answer("Связаться с нами можно через:\n"
"📧 Email: staff@blooooom.kz\n"
"📱 Telegram: @blooooom_support\n"
"📞 Телефон: +7 (708) 517-64-91")

@dp.message(F.web_app_data)
async def web_app_handler(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
        print(f"Получены данные от WebApp: {data}")
        logging.info(f"Получены данные от WebApp: {data}")  

        if data.get("success") and data.get("user_id"):
            await bot.send_message(data["user_id"], "✅ Ваш заказ успешно оформлен!")
    
    except Exception as e:
        logging.error(f"Ошибка при обработке данных WebApp: {e}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
