# kittybot/kittybot.py
import logging
import requests

from telebot import TeleBot, types


bot = TeleBot(token='7803181313:AAG_ramI-lOKIXqME67CJYiDACHkZQwtBRY')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
URL = 'https://api.thecatapi.com/v1/images/search'


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat_id = message.chat.id
    bot.send_photo(chat_id, get_new_image())


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('/newcat')
    keyboard.add(button)

    bot.send_message(
        chat_id=chat_id,
        text=f'Привет, {name}. Посмотри, какого котика я тебе нашел',
        reply_markup=keyboard,
    )

    bot.send_photo(chat_id, get_new_image())


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я Test_py3bot!')


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
