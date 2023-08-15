import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


logging.basicConfig(level=logging.INFO)

API_TOKEN = "6577800215:AAFD143UvazP2izf0x7edWThq-M1VRe75Gk"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Вітаю! Бот готовий взаємодіяти з вами.")
    await message.reply("Будь ласка, введіть ваш Логін:")



@dp.message_handler(commands=["get_data"])
async def get_data_from_drf(message: types.Message):
    response = requests.get('http://127.0.0.1:8000/api/books/')

    data = response.json()
    print(data[2])
    # Process the data and send a response
    await message.reply(f"Received data from DRF: {data[2]}")



@dp.message_handler(commands=['test'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id="@", text="test message")




# Call the 'sent' function to send a message when the bot starts
async def on_startup(dp):
    await sent()

executor.start_polling(dp, skip_updates=True)
