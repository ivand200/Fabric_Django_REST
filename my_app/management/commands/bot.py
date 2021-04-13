from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler, ConversationHandler
from telegram.ext import Updater
from telegram.utils.request import Request
from telegram import Location, ChatLocation, User,  ReplyKeyboardMarkup, ReplyKeyboardRemove
import datetime
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging
import sqlite3

from my_app.models import Survey
from my_app.models import User

COLOR, HOBBIES, OLD = range(3)

def start(update: Update, _: CallbackContext) -> int:
    reply_keyboard = [['Red', 'Blue', 'Orange', 'Black']]
    m = update.message
    username = update.message.from_user.username
    chat_id = update.effective_chat.id
    c, created = User.objects.get_or_create(name=chat_id)
    update.message.reply_text(
        'Hi! This is survey'
        f'What is your favorite color?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return COLOR


def color(update: Update, _: CallbackContext):
    reply_keyboard = [['Netflix', 'Reading', 'Drinking', 'Travel']]
    user = update.message.from_user
    chat_id = update.effective_chat.id
    m = update.message.text
    c, created = User.objects.get_or_create(name=chat_id)
    s = Survey(user = c, question = "What is your favorite color?", answer = m)
    s.save()
    update.message.reply_text(
        'Done! Now, Choose your hobbies',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return HOBBIES


def hobbies(update: Update, _: CallbackContext):
    user = update.message.from_user
    m = update.message.text
    chat_id = update.effective_chat.id
    m = update.message.text
    c, created = User.objects.get_or_create(name=chat_id)
    s = Survey(user = c, question = "Choose your hobbies", answer = m)
    s.save()
    update.message.reply_text(
        'Gorgeous! Now, please type your age.'
    )

    return OLD

def old(update: Update, _: CallbackContext):
    user = update.message.from_user
    m = update.message.text
    chat_id = update.effective_chat.id
    c, created = User.objects.get_or_create(name=chat_id)
    s = Survey(user = c, question = "Add your age", answer = m)
    s.save()
    update.message.reply_text(
        f"Thank you for your time!")

    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

class Command(BaseCommand):
    help = "Telegram-bot"

    def handle(self, *args, **options):
        request = Request( connect_timeout=0.5, read_timeout=0.5,)
        bot = Bot(request=request, token=settings.TOKEN)
        print(bot.get_me())

        updater = Updater(bot=bot, use_context=True,)

        back_handler = MessageHandler(Filters.text("Back"), start)
        updater.dispatcher.add_handler(back_handler)

        conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            COLOR: [MessageHandler(Filters.regex('^(Red|Blue|Orange|Black)$'), color)],
            HOBBIES: [MessageHandler(Filters.regex('^(Netflix|Reading|Drinking|Travel)$'), hobbies)],
            OLD: [MessageHandler(Filters.regex('[0-9]+'), old)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        )

        updater.dispatcher.add_handler(conv_handler)

        updater.start_polling()


        updater.idle()
