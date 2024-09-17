import asyncio
import os
import django
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command  # Импортируем фильтр Command
from aiogram.types import Message
import logging
logging.basicConfig(level=logging.DEBUG)

from django.conf import settings

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
django.setup()

from flowers.models import Order, Flower, User

API_TOKEN = '7470094368:AAFXHcaZOiQ7znB0A7rO40qqu4QgutRmN_M'
ADMIN_CHAT_ID = '-1002289833985'  # Вставьте ID чата администратора

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))  # Используем фильтр Command вместо commands=['start']
async def send_welcome(message: Message):
    await message.answer("Добро пожаловать! Этот бот предназначен для получения заказов на доставку цветов.")

def send_order_to_telegram(order):
    # Формирование сообщения с информацией о заказе
    order_details = f"Новый заказ!\nПользователь: {order.user.username}\nАдрес доставки: {order.delivery_address}\nСумма заказа: {order.total_price} руб."
    for flower in order.flowers.all():
        order_details += f"\nЦветок: {flower.name}, Цена: {flower.price} руб."

    # Отправка сообщения администратору
    asyncio.run(bot.send_message(ADMIN_CHAT_ID, order_details))

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
