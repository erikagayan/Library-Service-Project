import telebot
from django.core.management.base import BaseCommand
from library_config.settings import TELEGRAM_BOT_TOKEN


class TeleBot(BaseCommand):

    def send_borrow_book_notification(self, message):
        bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)
        bot.reply_to(message)

    def handle():
        bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)

        @bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            bot.reply_to(message, "Howdy, how are you doing?")

        @bot.message_handler(func=lambda message: True)
        def echo_all(message):
            bot.reply_to(message, message.text)

        bot.infinity_polling()


