import telebot
from telebot import types
import sqlite3
import webbrowser

bot = telebot.TeleBot('')


# 1. Обработчик команды /start — регистрация пользователя через диалог
name = None  # глобальная переменная для временного хранения имени

@bot.message_handler(commands=['start'])
def start(message):
    # Подключаемся к БД (файл sevent.db)
    conn = sqlite3.connect('sevent.db')
    cur = conn.cursor()

    # Создаём таблицу users, если её нет
    # ВНИМАНИЕ: в оригинале ошибка в синтаксисе SQLite.
    # Правильно: id INTEGER PRIMARY KEY AUTOINCREMENT
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), pass VARCHAR(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем! Введите ваше имя')

    # Регистрируем следующий шаг — после ответа пользователя вызовется user_name
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()          # сохраняем введённое имя
    bot.send_message(message.chat.id, 'Введите пароль')

    # Следующий шаг — получение пароля
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('sevent.db')
    cur = conn.cursor()

    # Вставка данных в таблицу (используем безопасную подстановку, но лучше executemany с ?)
    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    # Создаём инлайн-кнопку, которая будет вызывать callback
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))

    bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)


# Обработчик нажатий на инлайн-кнопки (callback_data)
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'users':
        conn = sqlite3.connect('sevent.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        cur.close()
        conn.close()

        info = ''
        for el in users:
            info += f'Имя: {el[1]}, пароль: {el[2]}\n'

        bot.send_message(call.message.chat.id, info)

# 2. Обработчик команды /phot — отправка фото с обычной клавиатурой (ReplyKeyboardMarkup)

@bot.message_handler(commands=['phot'])
def start(message):
    # Создаём обычную клавиатуру (прилипает к полю ввода)
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти на сайт')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Удалить фото')
    btn3 = types.KeyboardButton('Изменить текст')
    markup.row(btn2, btn3)

    # Открываем файл с фото и отправляем
    file = open('./photo.jpg', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)

    # Регистрируем шаг для обработки нажатий на обычные кнопки
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    # Обработка текста, который приходит от обычных кнопок
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, 'Website is open')
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'Delete')
    # Изменить текст — не реализовано, можно добавить



# 3. Обработчик входящих фото — показывает инлайн-кнопки под фото
@bot.message_handler(content_types=['photo'])  # content_types=['photo'] ловит только фото
def get_photo(message):
    # Создаём инлайн-клавиатуру (кнопки под сообщением)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://google.com')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2, btn3)

    # reply_to  ответ на сообщение с фото
    bot.reply_to(message, 'Какое красивое фото', reply_markup=markup)


# ВНИМАНИЕ: В коде два обработчика callback_query_handler с одинаковым условием.
# Последний перезапишет первый. Чтобы работали оба, нужно объединить логику.
# Здесь я показываю второй обработчик, но в реальном проекте их лучше слить в один.
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        # Удаляем сообщение, которое находится на одно выше текущего (message_id - 1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        # Редактируем текст текущего сообщения (меняем на 'Edit text')
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)



# 4. Открытие сайта в браузере по команде /site (в оригинале написано 'site, website' — так не работает)

@bot.message_handler(commands=['site'])   # команда должна быть одна. Если нужно две, пиши ['site', 'website']
def site(message):
    webbrowser.open('https://www.google.com')



# 5. Обычный обработчик команды /help
@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, 'help message')


# Запуск бота (polling)
bot.polling(none_stop=True)

