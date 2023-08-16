import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_config.settings")
django.setup()


from aiogram import executor
from django.apps import AppConfig
from telegram_bot.apps import dp
from telegram_bot import commands


class TelegramBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telegram_bot"


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
