import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from django.contrib.sites import requests

logging.basicConfig(level=logging.INFO)

# Замість 'YOUR_TOKEN' вставте свій токен бота, який ви отримали від @BotFather
API_TOKEN = '6577800215:AAFD143UvazP2izf0x7edWThq-M1VRe75Gk'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.INFO(f"{user_id=} {user_full_name=}")

    await message.reply(f"Привіт {user_full_name}! Я бот. Напишіть щось, і я повторю це.")

@dp.message_handler(commands=['get_data'])
async def get_data_from_drf(message: types.Message):
    try:
        # Make a GET request to your DRF API
        response = requests.get('http://your-drf-api-url/data/')
        data = response.json()

        # Process the data and send a response
        await message.reply(f"Received data from DRF: {data}")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
