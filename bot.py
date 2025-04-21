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

with open("translations.json", "r", encoding="utf-8") as file:
    translations = json.load(file)

user_languages = {}

def get_translation(user_id, key):
    lang = user_languages.get(user_id, "ru")
    return translations.get(lang, {}).get(key, key)

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    user_id = message.from_user.id
    user_languages[user_id] = "kk" 
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text=get_translation(user_id, "buttons.subscribe"),
                web_app=WebAppInfo(url=f"https://oljawave.github.io/bloom-tg-miniapp/?user_id={user_id}")
            )],
            [KeyboardButton(text=get_translation(user_id, "buttons.my_orders"))],
            [KeyboardButton(text=get_translation(user_id, "buttons.about_us"))],
            [KeyboardButton(text=get_translation(user_id, "buttons.contacts"))],
            [KeyboardButton(text=get_translation(user_id, "buttons.language"))]
        ],
        resize_keyboard=True
    )
    
    await message.answer(get_translation(user_id, "start"), reply_markup=keyboard)



@dp.message(F.text == "/delete")
async def delete_order(message: Message):
    user_id = message.from_user.id
    await message.answer("Пожалуйста, отправьте ID заказа для удаления.")


    @dp.message(F.text)
    async def handle_order_id(msg: Message):
        order_id = msg.text.strip()

        if not order_id.isdigit():
            await msg.answer("Пожалуйста, введите корректный ID заказа.")
            return

        response = requests.post(
            f"http://api.bloooom.kz:8443/orders/{order_id}/delete", 
            json={"chat_id": user_id}
        )
        
        if response.status_code == 200:
            await msg.answer(f"Заказ с ID {order_id} успешно удален.")
        else:
            await msg.answer(f"Ошибка: не удалось удалить заказ с ID {order_id}. Возможно, вы не имеете доступа.")



@dp.message(lambda message: message.text == get_translation(message.from_user.id, "buttons.language"))
async def change_language(message: Message):
    language_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇰🇿 Қазақша")],
            [KeyboardButton(text="🇷🇺 Русский")],
            [KeyboardButton(text="🇬🇧 English")]
        ],
        resize_keyboard=True
    )
    await message.answer(get_translation(message.from_user.id, "choose_language"), reply_markup=language_keyboard)



@dp.message(F.text.in_(["🇰🇿 Қазақша", "🇷🇺 Русский", "🇬🇧 English"]))
async def set_language(message: Message):
    user_id = message.from_user.id
    lang_map = {"🇰🇿 Қазақша": "kk", "🇷🇺 Русский": "ru", "🇬🇧 English": "en"}
    user_languages[user_id] = lang_map[message.text]

    # Создаем клавиатуру с основными кнопками
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text=get_translation(user_id, "buttons.subscribe"),
                web_app=WebAppInfo(url=f"https://oljawave.github.io/bloom-tg-miniapp/?user_id={user_id}")
            )],
            [KeyboardButton(text=get_translation(user_id, "buttons.my_orders"))],
            [KeyboardButton(text=get_translation(user_id, "buttons.about_us"))],
            [KeyboardButton(text=get_translation(user_id, "buttons.contacts"))],
            [KeyboardButton(text=get_translation(user_id, "buttons.language"))]  
        ],
        resize_keyboard=True
    )

    await message.answer(get_translation(user_id, "start"), reply_markup=keyboard)



@dp.message(lambda message: message.text == get_translation(message.from_user.id, "buttons.my_orders"))
async def my_orders(message: types.Message):
    user_id = message.from_user.id  
    response = requests.get(f"https://bloom-backend-production.up.railway.app/orders/{user_id}")  

    if response.status_code == 200:
        orders = response.json().get("orders", [])

        if not orders:
            await message.answer(get_translation(user_id, "no_orders"))
            return
        
        text = get_translation(user_id, "orders")
        for order in orders:
            text += get_translation(user_id, "order_details").format(
                order_id=order['order_id'],
                dates=', '.join(order['dates']),
                price_range=order['price_range'],
                address=order['address'],
                phone=order['phone']
            )
        
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer(get_translation(user_id, "no_orders"))

@dp.message(lambda message: message.text == get_translation(message.from_user.id, "buttons.about_us"))
async def about_handler(message: Message):
    await message.answer(get_translation(message.from_user.id, "about"))

@dp.message(lambda message: message.text == get_translation(message.from_user.id, "buttons.contacts"))
async def contacts_handler(message: Message):
    await message.answer(get_translation(message.from_user.id, "contacts"))

@dp.message(F.web_app_data)
async def web_app_handler(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
        logging.info(f"Получены данные от WebApp: {data}")  

        if data.get("success") and data.get("user_id"):
            await bot.send_message(data["user_id"], get_translation(data["user_id"], "order_success"))
    except Exception as e:
        logging.error(f"Ошибка при обработке данных WebApp: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())