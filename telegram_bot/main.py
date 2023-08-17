import os
import django
from aiogram import executor
from telegram_bot.apps import dp


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_config.settings")
django.setup()


from telegram_bot import commands


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
