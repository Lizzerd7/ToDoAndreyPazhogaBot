import telebot
from telebot import types

import time
import random

import sqlite3

bot = telebot.TeleBot('5810337686:AAHWBSQ0KTJkkyjvpUCvTlyArVc4_qMfMS8')


# 👉 🙏 👆 👇 😅 👋 🙌 ☺️ ❗ ️‼️ ✌️ 👌 ✊ 👨‍💻  🤖 😉  ☝️ ❤️ 💪 ✍️ 🎯  ⛔  ️✅ 📊📈🧮   🗳️


@bot.callback_query_handler(func=lambda call: True)
def step(call):

    if call.data == 'key1':
        pass

    elif call.data == 'key2':
        pass


@bot.message_handler(commands=['getmyid'])
def getmyid(message):
    ID = message.chat.id
    bot.send_message(message.chat.id, f'Ваш user ID: {ID}', parse_mode='Markdown')




@bot.message_handler(commands=['start'])
def start(message):
    ID = message.chat.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    message_text = f'Привет {first_name}!\nВаш user ID: {ID}\nВерно ли я узнал Вашу фамилию {last_name}?'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn0 = types.KeyboardButton('Добавить задачу')
    btn1 = types.KeyboardButton('Посмотреть список задач')
    markup.add(btn0, btn1)

    bot.send_message(message.chat.id, message_text, parse_mode='Markdown', reply_markup=markup)



@bot.message_handler(content_types=['text'])
def mess(message):
    get_message_bot = message.text.strip().lower()


    if get_message_bot == 'добавить задачу':

        con = sqlite3.connect('sqlite.db')
        cur = con.cursor()

        cur.execute('''
                           CREATE TABLE IF NOT EXISTS todo(
                               id INTEGER,  -- ID пользователя в телеграм
                               name TEXT,  -- имя пользователя
                               subject TEXT, -- предмет, который надо сделать
                               tasks TEXT,   -- записываем нашу задачу
                               data TEXT  -- формат даты 18.12.2022
                           );
                           ''')
        con.commit()


        bot.send_message(message.chat.id, f'Просто запишите свою задачу в формате: \n'
                                          f'[предмет; текст задачи; конец срока выполнения]')

        @bot.message_handler(content_types=['text'])
        def message_input(message):
            M = message.text.split(';')
            sub = M[0].strip()
            task = M[1].strip()
            data = M[2].strip()

            con = sqlite3.connect('sqlite.db')
            cur = con.cursor()

            cur.execute(f'SELECT * FROM todo WHERE id = {message.chat.id}')
            records = cur.fetchone()


            cur.execute('INSERT INTO todo VALUES(?, ?, ?, ?, ?);', (message.chat.id, message.from_user.first_name, sub, task, data))
            con.commit()


            con.close()



            bot.send_message(message.chat.id, f'🤖 Отлично, записал вашу задачу', parse_mode='Markdown')

        bot.register_next_step_handler(message, message_input)


    elif get_message_bot == 'посмотреть список задач':

        con = sqlite3.connect('sqlite.db')
        cur = con.cursor()

        cur.execute('''
                           CREATE TABLE IF NOT EXISTS todo(
                               id INTEGER,  -- ID пользователя в телеграм
                               name TEXT,  -- имя пользователя
                               subject TEXT, -- предмет, который надо сделать
                               tasks TEXT,   -- записываем нашу задачу
                               data TEXT  -- формат даты 18.12.2022
                           );
                           ''')

        cur.execute(f'SELECT subject, tasks, data FROM todo WHERE  id = {message.chat.id}')
        message_text = ''
        records = cur.fetchall()
        for row in records:
            message_text += f'------------------\n' \
                            f'*Тип:* {row[0]}\n' \
                            f'*Задача:* {row[1]}\n' \
                            f'*Срок до:* {row[2]}\n'
        bot.send_message(message.chat.id, message_text, parse_mode='Markdown')
        con.commit()

    else:
        bot.send_message(message.chat.id, f'У меня нет такой команды..но я еще учусь!', parse_mode='Markdown')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)
