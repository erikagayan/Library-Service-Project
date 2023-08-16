import logging
from django.apps import AppConfig
from library_config.settings import TELEGRAM_BOT_TOKEN
import requests
from aiogram import Bot, Dispatcher, executor, types
# from aiogram.utils import executor


logging.basicConfig(level=logging.INFO)


class TelegramBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telegram_bot"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["test"])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Нова апка телеграму, привіт apps")
