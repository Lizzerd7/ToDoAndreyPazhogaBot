import telebot  # после копирования проекта с github обязательно импортируем библиотеку telebot
from telebot import types  # предварительно его нужно скачать, введя в terminal команду pip install pyTelegramBotAPI

import time  # это дополнительные библиотеки встроенные в Python
import random

import sqlite3

bot = telebot.TeleBot('5810337686:AAHWBSQ0KTJkkyjvpUCvTlyArVc4_qMfMS8')  # сюда нужно вписать ваш API key от официального бота @BotFather


# 👉 🙏 👆 👇 😅 👋 🙌 ☺️ ❗ ️‼️ ✌️ 👌 ✊ 👨‍💻  🤖 😉  ☝️ ❤️ 💪 ✍️ 🎯  ⛔  ️✅ 📊📈🧮   🗳️
# просто вынес сюда некоторое количество эмоджи из телеграмма, можно спокойно встраивать в str сообщения


@bot.callback_query_handler(func=lambda call: True)  # данная функция обрабатывает call запросы от inline кнопок
def step(call):

    if call.data == 'game':  # если call.data запрос совпал, то исполняем этот скрипт
        M = ['+', '-']
        a = random.randint(1, 100)  # это не относится к библиотеке telebot, подробнее читайте про библиотеку random и ее методы
        s = random.choice(M)
        b = random.randint(1, 100)

        bot.send_message(call.message.chat.id, f'Решите пример {a} {s} {b} =', parse_mode='Markdown')  # выводим на экран пример, который пользователь должен решить

        if s == "+":  # если у нас зарандомился "+", то запускаем функцию обработки вводимого текста
            @bot.message_handler(content_types=['text'])  # то есть создаем эту функцию, если мы хотим обрабатывать повторное введенное пользователем сообщение
            def message_input(message):
                x = int(message.text)  # в переменную х положили введенное пользователем число и перевели в int

                if x == a + b:  # если пользователь ответил верно
                    bot.send_message(call.message.chat.id, f'Отлично, правильный ответ!', parse_mode='Markdown')
                else:  # иначе если ответил неверно
                    bot.send_message(call.message.chat.id, f'Ответ не верный..', parse_mode='Markdown')

            bot.register_next_step_handler(call.message, message_input)  # в конце обязательно надо функцию закрыть

        if s == "-":  # полностью аналогичная функция для минуса
            @bot.message_handler(content_types=['text'])
            def message_input(message):
                x = int(message.text)

                if x == a - b:
                    bot.send_message(call.message.chat.id, f'Отлично, правильный ответ!', parse_mode='Markdown')
                else:
                    bot.send_message(call.message.chat.id, f'Ответ не верный..', parse_mode='Markdown')

            bot.register_next_step_handler(call.message, message_input)

    elif call.data == 'other':  # условий на обработку call.data запросов может быть сколько угодно
        pass  # пока скрипт не доделан, пропускаем его


@bot.message_handler(commands=['getmyid'])  # пример создание команды, вызывать с именем /getmyid
def getmyid(message):
    ID = message.chat.id
    bot.send_message(message.chat.id, f'Ваш user ID: {ID}', parse_mode='Markdown')  # получили ID пользователя и вывели на экран через f-строку




@bot.message_handler(commands=['start'])  # Любой бот начинается с команды /start
def start(message):
    ID = message.chat.id  # в message.chat.id передается ID пользователя Telegram, он всегда публичен
    first_name = message.from_user.first_name  # Также можем получить имя и фамилию пользователя, если они не скрыты
    last_name = message.from_user.last_name

    message_text = f'Привет {first_name}!\nВаш user ID: {ID}\nВерно ли я узнал Вашу фамилию {last_name}?'  # используя f-строки можем делать удобные сообщения для бота

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # открываем разметку для Keyboard кнопок, указываем кол-во кнопок в строке через row_width
    btn0 = types.KeyboardButton('ToDo')
    btn1 = types.KeyboardButton('Привет')
    btn2 = types.KeyboardButton('Запустить функцию')
    btn3 = types.KeyboardButton('Бот отправляет фото')  # создаем кнопки
    btn4 = types.KeyboardButton('Разметка текста')
    btn5 = types.KeyboardButton('Создать кнопки inline')
    markup.add(btn0, btn1, btn2, btn3, btn4, btn5)  # и добавляем их к нашей разметки

    bot.send_message(message.chat.id, message_text, parse_mode='Markdown', reply_markup=markup)
    # бот отправляет сообщение: message_text
    # пользователю с id: message.chat.id,
    # при этом используя разметку: parse_mode='Markdown'
    # и опубликовывая нашу разметку с клавиатурными кнопками: reply_markup=markup


@bot.message_handler(content_types=['text'])  # это функция обрабатывающая все текстовые сообщения от пользователя
def mess(message):
    get_message_bot = message.text.strip().lower()  # полученную от пользователя строку (str) мы переводим в нижний регистр и убираем лишние пробелы

    if get_message_bot == 'todo':

        con = sqlite3.connect('sqlite.db')
        cur = con.cursor()

        cur.execute('''
                           CREATE TABLE IF NOT EXISTS todo(
                               id INTEGER,  -- ID пользователя в телеграм
                               name TEXT,  -- имя пользователя
                               subject TEXT -- предмет, который надо сделать
                               tasks TEXT,   -- записываем нашу задачу
                               data TEXT  -- формат даты 18.12.2022
                           );
                           ''')

        cur.execute(f'SELECT tasks, data FROM todo WHERE  id = {message.chat.id}')
        message_text = ''
        records = cur.fetchall()
        for row in records:
            message_text += f'{row[0]}, срок до: {row[1]}\n'
        bot.send_message(message.chat.id, message_text, parse_mode='Markdown')
        con.commit()




        bot.send_message(message.chat.id, f'Просто запишите свою задачу в формате: \n'
                                          f'[[предмет; текст задачи; конец срока выполнения]]', parse_mode='Markdown')
        @bot.message_handler(content_types=['text'])
        def message_input(message):
            M = message.text.split(';')
            text = M[0]
            data = M[1]

            con = sqlite3.connect('sqlite.db')
            cur = con.cursor()

            cur.execute(f'SELECT * FROM todo WHERE id = {message.chat.id}')
            records = cur.fetchone()


            cur.execute('INSERT INTO todo VALUES(?, ?, ?, ?);', (message.chat.id, message.from_user.first_name, text, data))
            con.commit()


            con.close()



            bot.send_message(message.chat.id, f'🤖 Отлично, записал вашу задачу', parse_mode='Markdown')

        bot.register_next_step_handler(message, message_input)




    # region Команды для рассмотрения, прочитай комментарии и попробуй поиграться с ними
    elif get_message_bot == "привет":  # если пользователь нажал кнопку или написал "Привет", то запускается этот скрипт
        bot.send_message(message.chat.id, f'Hi! How are you?', parse_mode='Markdown')  # Просто отвечаем пользователю на его сообщение

    elif get_message_bot == 'запустить функцию':  # если пользователь нажал кнопку или написал "Запустить функцию", то запускается этот скрипт
        bot.send_message(message.chat.id, f'Для демонстрации нажмите 👉 /getmyid', parse_mode='Markdown')  # в сообщение через /command мы запускаем команду описанную в строке 51 этого файла

    elif get_message_bot == 'создать кнопки inline':  # если пользователь нажал кнопку или написал "Cоздать кнопки inline", то запускается этот скрипт
        markup = types.InlineKeyboardMarkup(row_width=1)  # создаем разметку с типом клавиш inline, по одной клавише в строке и add добавляем клавиши на разметку markup
        markup.add(types.InlineKeyboardButton("Ссылка на мой Telegram канал", url="https://t.me/itpy_easy_ege"),  # данная кнопка просто переносит ссылку url
                   types.InlineKeyboardButton("Хочу решить пример", callback_data='game'))  # а эта кнопка запускает обработку события под именем game в функции из строки 14 файла main.py
        bot.send_message(message.chat.id, f'К сожалению без какого-либо bot.send нельзя отправить markup кнопки', reply_markup=markup)  # обязательно пишем reply_markup=markup, чтобы опубликовать кнопки

    elif get_message_bot == 'бот отправляет фото':  # если пользователь нажал кнопку или написал "Бот отправляет фото", то запускается этот скрипт
        pic1 = open('photo/Diploma.png', 'rb')
        bot.send_photo(message.chat.id, pic1)
        bot.send_message(message.chat.id, f'Смотрите какой у меня красивый Диплом XD')

        pic2 = open('photo/report.png', 'rb')
        pic3 = open('photo/oficial.png', 'rb')
        pic4 = open('photo/price.png', 'rb')
        bot.send_media_group(message.chat.id, [types.InputMediaPhoto(pic2),
                                               types.InputMediaPhoto(pic3),
                                               types.InputMediaPhoto(pic4)])
        bot.send_message(message.chat.id, f'А сейчас я @ilandroxy работаю репетитором по Информатике и Программированию Python')

    elif get_message_bot == 'разметка текста':  # если пользователь нажал кнопку или написал "Разметка текста", то запускается этот скрипт
        bot.send_message(message.chat.id, f'Для разметки нужно использовать [parse_mode]="Markdown" или [parse_mode]="HTML"\n\n'
                                          f'Пример разметки Markdown:\n'
                                          f'– *Жирный шрифт*\n'
                                          f'– _Курсив_\n'  # здесь Вы можете видеть примеры использования разметки Markdown 
                                          f'– `для программ print(5 ** 2)`\n'
                                          f'– Ссылка на [мой блог Teletype](https://teletype.in/@ilandroxy)\n\n'  # не забываем подписаться на мой Teletype блог
                                          f'Можно было дописать [disable_web_page_preview=True], чтобы скрыть превью ссылки 😅', parse_mode='Markdown')
    # endregion Команды для рассмотрения, прочитай комментарии и попробуй поиграться с ними

    else:  # если пользователь ввел что-то неприличное, то отвечать мы не будем
        bot.send_message(message.chat.id, f'У меня нет такой команды..но я еще учусь!', parse_mode='Markdown')  # если на вход пользователь отправит что-то бредовое


if __name__ == '__main__':
    while True:  # запускаем бесконечный цикл
        try:  # пробуем наладить связь с сервером Telegram
            bot.polling(none_stop=True)  # polling отправляет запросы на сервара
        except Exception as e:  # если произойдет ошибка, то
            time.sleep(3)  # подождать 3 секунды
            print(e)  # и вывести logi ошибки в консоль компьютера

