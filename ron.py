import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Помощь'), KeyboardButton(text='Мой профиль')]],
        resize_keyboard=True
    )
    await message.answer('Привет! Нажми "Помощь" если нужна помощь или "Мой профиль" для информации о себе.',
                         reply_markup=keyboard)


@dp.message(Command('myid'))
async def cmd_myid(message: Message):
    user = message.from_user
    status = "⭐ Премиум" if user.is_premium else "✅ Обычный"

    # Экранируем специальные символы для Markdown
    def escape_markdown(text):
        if not text:
            return "Не указан"
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text

    first_name = escape_markdown(user.first_name)
    username = escape_markdown(f"@{user.username}") if user.username else "Не указан"

    profile_info = (
        f"📊 *Ваш профиль:*\n\n"
        f"🆔 *ID:* `{user.id}`\n"
        f"👤 *Имя:* {first_name}\n"
        f"🏷️ *Юзернейм:* {username}\n"
        f"⭐ *Статус:* {status}\n"
        f"🌐 *Язык:* {user.language_code.upper() if user.language_code else 'Не указан'}"
    )

    await message.answer(profile_info, parse_mode='MarkdownV2')


@dp.message(lambda message: message.text == 'Мой профиль')
async def profile_button(message: Message):
    await cmd_myid(message)


@dp.message(lambda message: message.text == 'Помощь')
async def help_button(message: Message):
    await message.answer(
        'Вот что я умею:\n/start - Показать приветствие\n/myid - Показать ваш ID, имя и статус\n/help - Показать эту справку')


@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Доступные команды:\n/start - Начать\n/myid - Показать ваш ID, статус и имя\n/help - Помощь')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')