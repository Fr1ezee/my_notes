import telebot
import requests
import json
bot = telebot.TeleBot('8924391274:AAHL_p2aKevSiZpaEmnVkE095ovf55piiDQ')
API = 'd99d4c8f3764fcb1c6e4fa87a018345b'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Привет рад тебя видеть Напиши название города')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
     data = json.loads(res.text)
     temp = data['main']['temp']
     bot.reply_to(message, f'Сейчас погода : {temp}')
     image = 'kyousuke.jpg' if temp > 5.0 else 'fet.jpg'
     file = open('./' + image, 'rb')
     bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Город указан неверно')




bot.polling(none_stop=True)