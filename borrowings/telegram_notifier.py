import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from library_config.settings import TELEGRAM_BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


async def send_notification(message):
    await bot.send_message(message)


@dp.message_handler(commands=["test"])
async def process_start_command(message: types.Message):

    await bot.send_message(message.from_user.id, "test message")


@dp.message_handler(commands=["hello"])
async def send_welcome(message: types.Message):
    await message.reply("Привіт, Я телеграм бот Бібліотеки ")


# executor.start_polling(dp, skip_updates=True)
