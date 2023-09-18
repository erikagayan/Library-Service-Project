import logging
from library_config.settings import TELEGRAM_BOT_TOKEN
from aiogram import Bot, Dispatcher

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
