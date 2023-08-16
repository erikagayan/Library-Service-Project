from datetime import date

import requests
from django.db.models import Sum
from borrowings.models import Borrowing
from books.models import Book
from telegram_bot import messages
from aiogram import types
from telegram_bot.apps import dp
from telegram_bot.apps import bot
from library_config.settings import JWT_TOKEN


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

user_response = ""


def recive_data(user_response):
    response = requests.get(
        "http://localhost:8000/api/borrowings/",
        headers={"Authorization": f"Bearer {JWT_TOKEN}"},
    )

    data = response.json()
    user_borrowed_books = []
    user_email = user_response
    for book in data:
        if book["user"] == user_email:
            user_borrowed_books.append(
                {
                    "id": book["id"],
                    "borrow_date": book["borrow_date"],
                    "expected_return_date": book["expected_return_date"],
                    "actual_return_date": book["actual_return_date"],
                    "book": book["book"],
                }
            )
    reply_text = ""
    if user_borrowed_books:
        reply_text += f"Borrowed books for {user_email}:\n"

        for book in user_borrowed_books:
            reply_text += (
                f"Book: {book['book']}\n"
                f"Borrow Date: {book['borrow_date']}\n"
                f"Expected Return Date: {book['expected_return_date']}\n"
                f"Actual Return Date: {book['actual_return_date']}\n\n"
            )
        return reply_text
    else:
        return f"No borrowed books found for {user_email}"


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("The bot is ready to interact with you.")
    await message.reply("Please enter your mailing address:")


@dp.message_handler(commands=["get_list_borrowing"])
async def get_data_from_drf(message: types.Message):
    # Process the data and send a response
    await message.reply(recive_data(user_response))


@dp.message_handler(lambda message: True)
async def handle_text(message: types.Message):
    global user_response
    user_response = message.text.strip()
    await message.reply(recive_data(user_response))
