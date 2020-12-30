# -*- coding: utf-8 -*-
import telebot
from telebot import types
from random import choice

# Инициализация
token = '1169969850:AAGUAhfgRvpd5jKvNNnkxZ2m5sjCDzUUImM'
my_chat_id = '579142036'
dope_chat_id = 'nowayiwouldpostthistogit'

bot = telebot.TeleBot(token)

# Клавиатура
markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
markup.row('Отправить бит')
markup.row('Какие биты НЕ нужны?')

# BOT REACTS TO HUMAN DIALOGUE (NOT CLICKBAIT)
@bot.message_handler(commands=['start'])
def reply_to_start(message):
    bot.send_message(message.chat.id, f"Здарова {message.from_user.first_name}", reply_markup=markup)


@bot.message_handler(commands=["send_beat"])
def reply_to_beat(message):
    bot.send_message(message.chat.id, 'Отправляй минусочек:')


@bot.message_handler(content_types=["text"])
def talk_to_me(message):  # Название функции ни на что не влияет лол
    if message.text == 'Отправить бит':
        reply_to_beat(message)
    elif message.text == 'Какие биты НЕ нужны?':
        bot.send_message(message.chat.id, 'ТОТАЛЬНЫЙ ЗАПРЕТ НА:\n' \
                                          '- дрилл биты\n' \
                                          '- тайп биты')
    else:
        # Доуп бот не разрешает тебе ругаться!
        string = message.text.lower()
        bad_words = ['хуй', 'блять', 'пизда','ебать', 'бля', 'сука', 'соси']
        if any(word in string for word in bad_words):
            reply = 'слыш у нас тут все культурно, понял?'
        else:
            reply = f"{message.from_user.first_name} бро ты базаришь с ботом, окстись!"
        bot.send_message(message.chat.id, reply)


@bot.message_handler(content_types=['audio'])
def respond_to_audio(message):
        bot.forward_message(dope_chat_id, message.chat.id, message.message_id)
        bot.send_message(dope_chat_id, f'@{message.from_user.username}')

if __name__ == '__main__':
    bot.infinity_polling()

