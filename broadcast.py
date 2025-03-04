import asyncio
import logging
from aiogram import Bot

TOKEN = "7656620027:AAFMvmxiOqelHS3hC2IwsaWthlAg3DxRPmA"
user_ids = [461357308]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)

async def send_broadcast():
    message_text = "🔔 Обновление! Теперь у нас можно выбрать язык бота. Перезапусти /start"
    
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, message_text)
            await asyncio.sleep(0.5)
        except Exception as e:
            logging.error(f"Ошибка при отправке {user_id}: {e}")

async def main():
    await send_broadcast()

if __name__ == "__main__":
    asyncio.run(main())
