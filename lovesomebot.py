# -*- coding: utf-8 -*-
import telebot
from telebot import types
from random import choice

# Инициализация
token = '1228572854:AAFUthtDS3OFNwlR82Si-FqXGergPxrD-gQ'
my_chat_id = '579142036'
daha_chat_id = 'noway'

bot = telebot.TeleBot(token)

# Клавиатура
markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
markup.row('Отправить бит', 'Не отправить бит')
markup.row('Какие биты нужны?')

# BOT REACTS TO HUMAN DIALOGUE (NOT CLICKBAIT)
@bot.message_handler(commands=['start'])
def reply_to_start(message):
    bot.send_message(message.chat.id, "Здарова бандит, че будем с тобой делать?", reply_markup=markup)


@bot.message_handler(commands=["send_beat"])
def reply_to_beat(message):
    bot.send_message(message.chat.id, 'Жги:')


@bot.message_handler(content_types=["text"])
def talk_to_me(message):  # Название функции ни на что не влияет лол
    if message.text == 'Отправить бит':
        reply_to_beat(message)
    elif message.text == 'Какие биты нужны?':
        bot.send_message(message.chat.id, '- чтоб хотелось трясти жопой\n' \
                                          '- чтоб хотелось быстро ехать на тачке\n' \
                                          '- чтоб хотелось бежать в слоу мо')
    elif message.text == 'Не отправить бит':
        bot.send_message(message.chat.id, 'ну и не надо')
    else:
        # Лавсам бот не разрешает тебе ругаться!
        string = message.text.lower()
        bad_words = [
            'хуй', 'блять', 'пизда','ебать', 'бля', 'сука', 'соси',
            'ебанашка', 'ебанутая', 'ебланка', 'уебанка', 'уеба',
            'уебище', 'уебись ', 'член', 'сосать',
        ]
        bad_questions =['когда альбом', 'когда релиз', 'когда новый музон', 'когда новая музыка', 'когда дроп']
        if any(word in string for word in bad_words):
            reply = 'Ой щас по жопе прилетит кому-то за такие слова...'
        elif any(word in string for word in bad_questions):
            reply = choice(['Скоро', 'В будущем'])
        else:
            reply = random_reply(message)
        bot.send_message(message.chat.id, reply)

def random_reply(message):
    r_dict = ['Когда новый альбом?',
                'Как лечь спать до 7 утра? А, точно, боты никогда не спят(',
                'Itwasreal или пиздишь??',
                f'{message.from_user.first_name}, ты понимаешь что разговариваешь с ботом?',
                'Сегодня было много битов, но я отправил маме только те, которые мне понравились😈',
              'Сама такая',
              'Лешго лешго погнали',
              'А ты точно продюсер?',
              'Ща все маме расскажу',
              'Не грусти - мама тебя любит',
              'Некомильфо',
              'Садись, 2',
              'Иди подумай над своим поведением',
              'Мясо',
              'Ууу-ля-ля',
              'Сиди дома, без причины квартиру не покидай'
    ]
    return choice(r_dict)

@bot.message_handler(content_types=['audio'])
def respond_to_audio(message):
        bot.forward_message(daha_chat_id, message.chat.id, message.message_id)
        bot.send_message(daha_chat_id, f'@{message.from_user.username}')

if __name__ == '__main__':
    bot.infinity_polling()

