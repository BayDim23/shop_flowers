import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging
logging.basicConfig(level=logging.DEBUG)

API_TOKEN = '7470094368:AAFXHcaZOiQ7znB0A7rO40qqu4QgutRmN_M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Ваш chat_id: {chat_id}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())