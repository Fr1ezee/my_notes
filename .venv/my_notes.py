# КНОПКИ
# Inline кнопка:
btn = InlineKeyboardButton(text="Текст", callback_data="data")
# Reply кнопка (как меню снизу):
btn2 = KeyboardButton(text="Кнопка")

#ID пользователя
user_id = message.from_user.id
username = message.from_user.username

#База данных (sqlite3)
import sqlite3
conn = sqlite3.connect('mybot.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))