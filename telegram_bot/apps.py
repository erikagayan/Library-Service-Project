import logging
from django.apps import AppConfig
from library_config.settings import TELEGRAM_BOT_TOKEN
from aiogram import Bot, Dispatcher, types


logging.basicConfig(level=logging.INFO)


class TelegramBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telegram_bot"


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
