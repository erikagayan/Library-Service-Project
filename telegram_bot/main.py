from aiogram import executor
from telegram_bot.apps import dp
from telegram_bot import commands


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
