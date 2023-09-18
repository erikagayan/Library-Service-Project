import os
import django
import logging
from library_config.settings import TELEGRAM_BOT_TOKEN
from aiogram import Bot, Dispatcher


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_config.settings")
django.setup()


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
