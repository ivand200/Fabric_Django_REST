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

COLOR, HOBBIES, OLD, QUALITY = range(4)


def start(update: Update, _: CallbackContext):
    """START Survey, FIRST QUETIOS"""
    reply_keyboard = [['Red'], ['Blue'], ['Orange'], ['Black']]
    m = update.message
    username = update.message.from_user.username
    chat_id = update.effective_chat.id
    c, created = User.objects.get_or_create(name=chat_id)
    update.message.reply_text(
        'Hi! This is survey, please answer few questions\n\n'
        f'<b>What is your favorite color?</b>',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
                                          parse_mode=telegram.ParseMode.HTML
    )
    return COLOR


def color(update: Update, _: CallbackContext):
    """SECOND QUESTION"""
    reply_keyboard = [['Netflix'], ['Reading'], ['Drinking'], ['Travel']]
    user = update.message.from_user
    chat_id = update.effective_chat.id
    m = update.message.text
    c, created = User.objects.get_or_create(name=chat_id)
    s = Survey(user = c, question = "What is your favorite color?", answer = m)
    s.save()
    update.message.reply_text(
        'Done!\n<b>Choose your favorite hobby</b>',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
                                          parse_mode=telegram.ParseMode.HTML
                                          )
    return HOBBIES


def hobbies(update: Update, _: CallbackContext):
    """THIRD QUESTION"""
    user = update.message.from_user
    m = update.message.text
    chat_id = update.effective_chat.id
    m = update.message.text
    c, created = User.objects.get_or_create(name=chat_id)
    s = Survey(user = c, question = "Choose your hobby", answer = m)
    s.save()
    update.message.reply_text(
        'Cool!\n <b>Now, please type your age.</b>', parse_mode=telegram.ParseMode.HTML
    )
    return OLD


def old(update: Update, _: CallbackContext):
    """FOURTH QUESTION, END OF SURVEY"""
    user = update.message.from_user
    m = update.message.text
    chat_id = update.effective_chat.id
    c, created = User.objects.get_or_create(name=chat_id)
    s = Survey(user = c, question = "Add your age", answer = m)
    s.save()
    update.message.reply_text(
        f"Thank you,\n <b>Now type your best personal qualities (2-3)</b>\n"
        f"<i>Example:\nPatience, Courage...</i>", parse_mode=telegram.ParseMode.HTML)
    return QUALITY


def regular (update: Update, _: CallbackContext):
    user = update.message.from_user
    m = update.message.text
    chat_id = update.effective_chat.id
    m = update.message.text
    chat_id = update.effective_chat.id
    c, created = User.objects.get_or_create(name=chat_id)
    s = Survey(user = c, question = "type your best personal qualities", answer = m.lower())
    stat = Survey.objects.filter(user=c).order_by("-created_at")[:4]
    lst = list()
    list_str = "\n".join(str(item) for item in stat)
    cart_clear = list_str.replace('(','').replace(')','').replace(',','').replace('[','').replace(']','')
    s.save()
    update.message.reply_text(
        f"<b><u>Your answers:</u></b>\n{cart_clear}\n\nTo repeat survey use command /start",
        parse_mode=telegram.ParseMode.HTML)
    return ConversationHandler.END

def cancel(update: Update, _: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(
        'use command /start to start again', reply_markup=ReplyKeyboardRemove()
    )


def stat(update: Update, _: CallbackContext):
    user = update.message.from_user
    chat_id = update.effective_chat.id
    c, created = User.objects.get_or_create(name=chat_id)
    s = Survey.objects.filter(user=c).order_by("-created_at")[:4]
    lst = list()
    list_str = "\n".join(str(item) for item in s)
    cart_clear = list_str.replace('(','').replace(')','').replace(',','').replace('[','').replace(']','')
    update.message.reply_text(
        f'{cart_clear}.', reply_markup=ReplyKeyboardRemove()
    )

class Command(BaseCommand):
    help = "Telegram-bot"

    def handle(self, *args, **options):
        request = Request( connect_timeout=0.5, read_timeout=0.5,)
        bot = Bot(request=request, token=settings.TOKEN)
        print(bot.get_me())

        updater = Updater(bot=bot, use_context=True,)

        stat_handler = MessageHandler(Filters.text("Statistics"), stat)
        updater.dispatcher.add_handler(stat_handler)

        conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            COLOR: [MessageHandler(Filters.regex('^(Red|Blue|Orange|Black)$'), color)],
            HOBBIES: [MessageHandler(Filters.regex('^(Netflix|Reading|Drinking|Travel)$'), hobbies)],
            OLD: [MessageHandler(Filters.regex('[0-9]+'), old)],
            QUALITY: [MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')), regular)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        )

        updater.dispatcher.add_handler(conv_handler)

        updater.start_polling()


        updater.idle()
