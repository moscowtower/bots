# -*- coding: utf-8 -*-
import telebot
from telebot import types
from random import choice
import scp_parser
import requests
from bs4 import BeautifulSoup
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

# Инициализация
token = '804073989:AAFBmwDc9jhJVVNGmTnrnlEeGAvbSstvxGs'

my_chat_id = '579142036'

bot = telebot.TeleBot(token)

# Клавиатура
markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
markup.row('/random')

random_url = 'http://scpdb.org/wikidot_random_page'
def get_url(random_url):
  r = requests.get(random_url)
  url = r.url
  return url


# BOT REACTS TO HUMAN DIALOGUE (NOT CLICKBAIT)
@bot.message_handler(commands=['start'])
def reply_to_start(message):
    bot.send_message(message.chat.id, f"Привет, почитаем SCP, {message.from_user.first_name}?", reply_markup=markup)


@bot.message_handler(commands=["random"])
def send_new_scp(message):
    url = get_url(random_url)
    title = scp_parser.get_title(url)
    format_title = str('*' + title + '*')
    print(title)
    img = str(scp_parser.get_img(url))
    print(img)
    text = scp_parser.get_text(url)

    if title:
        bot.send_message(message.chat.id, format_title, parse_mode='Markdown')
    if img != 'None':
        bot.send_photo(message.chat.id, img)

    if len(text) >= 16256:
        part = len(text)//4
        text1 = text[:part]
        text2 = text[part:part * 2]
        text3 = text[part * 2: part * 3]
        text4 = text[part * 3:]
        send_text(text1, message)
        send_text(text2, message)
        send_text(text3, message)
        send_text(text4, message)
    else:
        if len(text) >= 8128:
            part = len(text) // 2
            text1 = text[:part]
            text2 = text[part:]
            send_text(text1, message)
            send_text(text2, message)
        else:
            send_text(text, message)

def send_text(text, message):
    print(len(text))
    if len(text) > 0:
        if len(text) < 4096:
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
        else:
            if len(text)//2 >= 8128:
                part = len(text) // 8
                bot.send_message(message.chat.id, text[:part], parse_mode='Markdown')
                bot.send_message(message.chat.id, text[part:part * 2], parse_mode='markdown')
                bot.send_message(message.chat.id, text[part * 2:part * 3], parse_mode='markdown')
                bot.send_message(message.chat.id, text[part * 3:part * 4], parse_mode='markdown')
                bot.send_message(message.chat.id, text[part * 4:part * 5], parse_mode='markdown')
                bot.send_message(message.chat.id, text[part * 5:part * 6], parse_mode='markdown')
                bot.send_message(message.chat.id, text[part * 6:part * 7], parse_mode='markdown')
                bot.send_message(message.chat.id, text[part * 7:], parse_mode='markdown')
            else:
                if len(text)//2 >= 4096:
                    part = len(text) // 4
                    bot.send_message(message.chat.id, text[:part], parse_mode='Markdown')
                    bot.send_message(message.chat.id, text[part:part * 2], parse_mode='markdown')
                    bot.send_message(message.chat.id, text[part * 2:part * 3], parse_mode='markdown')
                    bot.send_message(message.chat.id, text[part * 3:], parse_mode='markdown')
                else:
                    part = len(text) // 2
                    bot.send_message(message.chat.id, text[:part], parse_mode='Markdown')
                    bot.send_message(message.chat.id, text[part:], parse_mode='markdown')

@bot.message_handler(content_types=["text"])
def find_the_scp(message):
    title = scp_parser.find_title(message.text)
    if type(message.text) != 'String':
        pass
    format_title = str('*' + title + '*')
    pic = str(scp_parser.find_img(message.text))
    url = 'http://scpfoundation.net/scp-' + str(message.text)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.title.string == 'The SCP Foundation':
        bot.send_message(message.chat.id, 'Страница не существует')
        return
    text = scp_parser.get_text(url)
    print(url)
    if title:
        bot.send_message(message.chat.id, format_title, parse_mode='markdown')
    else:
        bot.send_message(message.chat.id, text='Не получилось спарсить :(')
    if pic != 'None':
        bot.send_photo(message.chat.id, pic)
    if len(text) > 8128:
        part = len(text)//2
        text1 = text[:part]
        text2 = text[part:]
        send_text(text1, message)
        send_text(text2, message)
    else:
        send_text(text, message)


if __name__ == '__main__':
    bot.infinity_polling()

