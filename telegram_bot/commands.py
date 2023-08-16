from datetime import date
from django.db.models import Sum
from borrowings.models import Borrowing
from books.models import Book
from telegram_bot import messages
from aiogram import types
from telegram_bot.apps import dp
from telegram_bot.apps import bot


@dp.message_handler(commands=["help"])
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, messages.WELCOME_MESSAGE)


@dp.message_handler(commands=["test"])
async def process_start_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        "Новаbq бот Бібліотеки, привіт!"
    )


today = date.today()
count_borrowing_today = Borrowing.objects.filter(borrow_date=today).count()
count_borrowing_total = Borrowing.objects.count()
count_returned_today = Borrowing.objects.filter(
    actual_return_date=today).count()
count_available_book_total = Book.objects.aggregate(total=Sum("inventory"))
count_number_of_titles = Book.objects.distinct().count()


@dp.message_handler(commands="borrowing_today")
async def borrowing_today_handler(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        f"borrowed today: {count_borrowing_today}"
    )


@dp.message_handler(commands="borrowing_total")
async def borrowing_total(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        f"borrowed total: {count_borrowing_total}"
    )


@dp.message_handler(commands="returned_today")
async def returned_today(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        f"returned today: {count_returned_today}"
    )


@dp.message_handler(commands="available_books")
async def available_books_total(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        f"available_books: {count_available_book_total['total']}"
    )


@dp.message_handler(commands="number_of_titles")
async def count_titles(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        f"number of titles: {count_number_of_titles}"
    )
