# flower_shop/bot.py
import asyncio
import os
import django
from aiogram import Bot, Dispatcher, types

from django.conf import settings

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
django.setup()

from flowers.models import Order, Flower, User

API_TOKEN = '7470094368:AAFXHcaZOiQ7znB0A7rO40qqu4QgutRmN_M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Добро пожаловать в сервис доставки цветов! Используйте команду /order для оформления заказа.")


@dp.message(commands=['order'])
async def create_order(message: types.Message):
    user, created = User.objects.get_or_create(username=message.from_user.username)
    flowers = Flower.objects.all()
    flower_list = "\n".join([f"{flower.id}. {flower.name} - {flower.price} руб." for flower in flowers])

    if not flowers:
        await message.reply("В нашем магазине пока нет цветов.")
        return

    await message.reply(f"Выберите цветок, отправив его номер:\n{flower_list}")

    @dp.message(lambda msg: msg.text.isdigit())
    async def process_order(msg: types.Message):
        flower_id = int(msg.text)
        try:
            flower = Flower.objects.get(id=flower_id)
            order = Order.objects.create(user=user)
            order.flowers.add(flower)
            await message.reply(f"Ваш заказ на {flower.name} оформлен!")
        except Flower.DoesNotExist:
            await message.reply("Неправильный номер цветка. Попробуйте снова.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())