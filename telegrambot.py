# Этот кусок кода запускается, когда пользователь пишет /start
import telebot
import requests
import json
from config import BOT_TOKEN, API

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # Бот приветствует и просит написать название города
    bot.send_message(message.chat.id, 'Привет рад тебя видеть Напиши название города')

# Этот обработчик ловит все текстовые сообщения (которые не команды)
@bot.message_handler(content_types=['text'])
def get_weather(message):
    # Берём текст от пользователя, убираем лишние пробелы и приводим к нижнему регистру
    city = message.text.strip().lower()
    # Отправляем запрос к сайту openweathermap.org, чтобы получить погоду в этом городе
    # API - это твой секретный ключ (должен быть объявлен выше)
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    # Если город найден (статус ответа 200)
    if res.status_code == 200:
        # Разбираем полученный JSON-ответ в словарь
        data = json.loads(res.text)
        # Достаём температуру из поля main -> temp
        temp = data['main']['temp']
        # Отвечаем пользователю: какая сейчас температура
        bot.reply_to(message, f'Сейчас погода : {temp}')
        # Выбираем имя картинки: если температура выше 5 градусов - одну, если ниже или равно - другую
        image = 'kyousuke.jpg' if temp > 5.0 else 'fet.jpg'
        # Открываем файл с картинкой
        file = open('./' + image, 'rb')
        # Отправляем фото в чат
        bot.send_photo(message.chat.id, file)
    else:
        # Если город не найден (статус не 200)
        bot.reply_to(message, 'Город указан неверно')

# Запускаем бота, чтобы он постоянно слушал сообщения
bot.polling(none_stop=True)