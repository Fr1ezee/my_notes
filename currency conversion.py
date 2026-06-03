import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет введите сумму')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())

        if amount > 0:
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
            btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
            btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
            btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Число должно быть больше 0. Введите сумму')
            bot.register_next_step_handler(message, summa)

    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат, введите сумму')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        try:
            res = currency.convert(amount, values[0], values[1])
            bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)} {values[1]}')
        except:
            bot.send_message(call.message.chat.id, 'Ошибка конвертации')
    else:
        bot.send_message(call.message.chat.id, 'Введите пару валют через слэш (например: USD/EUR)')
        bot.register_next_step_handler(call.message, other_currency)


def other_currency(message):
    try:
        values = message.text.strip().upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)} {values[1]}')
    except Exception as e:
        bot.send_message(message.chat.id, 'Что-то пошло не так. Проверьте правильность ввода')


bot.polling(none_stop=True)
