from datetime import date
from borrowings.models import Borrowing
from telegram_bot import messages
from aiogram import types
from telegram_bot.apps import dp
from telegram_bot.apps import bot


@dp.message_handler(commands=["help"])
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, messages.WELCOME_MESSAGE)


@dp.message_handler(commands=["test"])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Нова апка телеграму, привіт apps")


today = date.today()
count_borrowing_today = Borrowing.objects.filter(borrow_date=today).count()


@dp.message_handler(commands="borrowing_today")
async def borrowing_today_handler(message: types.Message):
    await bot.send_message(message.from_user.id, f"borrowed today: {count_borrowing_today}")