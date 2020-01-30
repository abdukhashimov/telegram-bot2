# importing
import os
import logging
# import json
from emoji import emojize
from gettext import gettext as _, translation

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters
)
# end of imporitn

users = {}


class KeyboardLanguage(object):
    available_languages = ['en', 'uz', 'ru']
    language_op = 'en'

    def __init__(self, language_option):
        self.language = language_option

    @property
    def language(self):
        return self.language_op

    @language.setter
    def language(self, language_option):
        """Save the language if it is available"""
        if language_option in self.available_languages:
            self.language_op = language_option
        else:
            raise ValueError('Language that you chose is not available yet.')

    def install_language(self):
        self.lang = translation(self.language_op, localedir='locale',
                                languages=self.available_languages)
        self.lang.install()
        _ = self.lang.gettext
        return _


class Button(object):
    callback_data = None
    checkbox = ':white_check_mark:'
    inline = None
    checked = False

    def __init__(self, name, callback_data):
        self.name = name
        self.callback_data = callback_data
        self.__make_button()

    def __make_button(self):
        self.inline = InlineKeyboardButton(
            self.name, callback_data=str(self.callback_data))

    def __add_check_box(self, callback_data):
        self.inline = InlineKeyboardButton("{} {}".format(
            emojize(self.checkbox, use_aliases=True), self.name),
            callback_data=str(callback_data)
        )

    def __remove_check_box(self, callback_data):
        self.inline = InlineKeyboardButton(
            self.name, callback_data=str(callback_data))

    def toggle(self, callback_data):
        if self.checked:
            self.__remove_check_box(callback_data)
        else:
            self.__add_check_box(callback_data)
        self.checked = not self.checked

    @property
    def inline_pr(self):
        return self.inline

    @property
    def button_name_pr(self):
        return self.name

    @property
    def callback_data_pr(self):
        return self.callback_data

    def __str__(self):
        return str(self.inline)


class Keyboard(object):
    __services = [
        'Logo Design',
        'Web Development',
        'Mobile Development',
        'Telegram Bot',
        'SEO Optimization',
        'Ecommerce',
        'CRM'
    ]
    keyboard = []

    def start_keyboard(self):
        if len(self.keyboard) == 0:
            for index, name in enumerate(self.__services):
                self.keyboard.append(Button(_(name), str(index)))

    def get_keyboard(self):
        return self.keyboard


class User(object):
    def __init__(self, username, first_name, last_name):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.lang_opt = KeyboardLanguage('en')
        self.keyboard = Keyboard()

    @property
    def pr_username(self):
        return self.username

    @property
    def pr_first_name(self):
        return self.first_name

    @property
    def pr_last_name(self):
        return self.last_name

    def __str__(self):
        return "username: {}\nfirst_name: {}\nlast_name: {}".format(
            self.username,
            self.first_name,
            self.last_name
        )


SETUP, START = range(2)
logo_design, web_development, mobile_development, telegram_bot, \
    seo_optimization, ecommerce, crm = range(7)

# 'Logo Design',
# 'Web Development',
# 'Mobile Development',
# 'Telegram Bot',
# 'SEO Optimization',
# 'Ecommerce',
# 'CRM'
# helper functions


def get_user_from_id(user_id):
    global users
    user = users.get(user_id, None)
    return user


def update_user_from_id(user_id, my_user):
    global users
    users[user_id] = my_user
# end of the helper functions


def setup(update, context):
    global users
    user = update.message.from_user
    my_user = User(user.username, user.first_name, user.last_name)
    users[user.id] = my_user
    update.message.reply_text(
        'Please choose your prefered language',
        reply_markup=ReplyKeyboardMarkup(
            [[element.upper() for element in
                my_user.lang_opt.available_languages]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return SETUP


def verify_setup(update, context):
    text = update.message.text
    user = update.message.from_user
    my_user = get_user_from_id(user.id)
    try:
        my_user.lang_opt.language = text.lower()
    except Exception as e:
        print(e)
        update.message.reply_text(
            'The option you set is not available yet.'
        )
        return SETUP

    update.message.reply_text(
        'Language: {}'.format(my_user.lang_opt.language.title()),
    )
    # we need to display the options of services

    markup = []
    # install the keyboard
    my_user.keyboard.start_keyboard()
    for button in my_user.keyboard.get_keyboard():
        markup.append([button.inline_pr])
    markup.append([InlineKeyboardButton('{} Done'.format(
        emojize(':ok:', use_aliases=True)), callback_data='done')])

    update.message.reply_text(
        'Please choose one of our services',
        reply_markup=InlineKeyboardMarkup(markup)
    )
    print(users)

    update_user_from_id(user.id, my_user)
    return START


def main_menu(update, context):
    query = update.callback_query
    user_id = query.message.chat.id
    my_user = get_user_from_id(user_id)
    keyboard = my_user.Keyboard.get_keyboard()
    bot = context.bot
    markup = []
    keyboard[int(query.data)].toggle(query.data)
    for button in keyboard:
        markup.append([button.inline_pr])
    
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=_("Please choose one of our services") + '\n',
        reply_markup=reply_markup
    )
    return START

def option_display(update, context, max=None):
    # I have to identify which inline button is pressed
    query = update.callback_query
    user_id = query.message.chat.id
    my_user = get_user_from_id(user_id)
    keyboard = my_user.keyboard.get_keyboard()
    bot = context.bot
    markup = []
    if query.data != 'done':
        print(query.data)
        keyboard[int(query.data)].toggle(query.data)
        print(keyboard[int(query.data)])

    for button in keyboard:
        markup.append([button.inline_pr])
    markup.append([InlineKeyboardButton('Done', callback_data='done')])
    reply_markup = InlineKeyboardMarkup(markup)

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=_("Please choose one of our services") + '\n',
        reply_markup=reply_markup
    )
    return START


def main():
    TOKEN = '1017586683:AAH9YvHhXuIrWRiQkz0VdbY6zJEkMe23l9c'
    NAME = 'greatsoftbot'
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', setup)],
        states={
            SETUP: [MessageHandler(Filters.regex(
                '^(RU|EN|UZ)$'), verify_setup),
                MessageHandler(Filters.text, setup)],
            START: [
                CallbackQueryHandler(
                    option_display, pattern=r"[0-6]|^done$"),
            ]
        },
        fallbacks=[CommandHandler('start', setup)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
