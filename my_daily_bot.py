import os
import asyncio
from aiogram import Bot, Dispatcher, types
from datetime import datetime, timedelta

API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Список пользователей
users = set()

@dp.message()
async def start_handler(message: types.Message):
    if message.text == '/start':
        users.add(message.from_user.id)
        await message.answer("Ты подписался на ежедневные сообщения! Жди рассылку.")

async def daily_broadcast():
    await asyncio.sleep(1)
    while True:
        now = datetime.now()
        target_time = now.replace(hour=10, minute=0, second=0, microsecond=0)
        if now > target_time:
            target_time += timedelta(days=1)
        await asyncio.sleep((target_time - now).total_seconds())
        for user_id in users:
            try:
                await bot.send_message(user_id, "Это твоё ежедневное сообщение!")
            except Exception as e:
                print(f"Ошибка отправки {user_id}: {e}")

async def main():
    # Запускаем задачу рассылки
    asyncio.create_task(daily_broadcast())
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
