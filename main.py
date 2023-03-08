import openai
from loguru import logger
import time
import datetime
import telebot
from config import *

openai.api_key = API

bot = telebot.TeleBot(TOKEN)

logger.add('logs.log', format='{level} | {message}', level='INFO', rotation='1 MB', compression='zip')

current_date = datetime.datetime.now()


@bot.message_handler(commands=['start'])
def starter(message):
    bot.reply_to(message, 'Привет!\nЯ ChatGPT Telegram Bot \U0001F916\n'
                          'Задай мне любой вопрос и я постараюсь на него ответить')


@bot.message_handler(func=lambda _: True)
def reply(message: telebot.types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logger.info(f'{user_id=} | {user_name=} | {message.text=} | {time.asctime()}')

    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"Ты помощник, который отвечает на все. Текущая дата {current_date}"},
        {"role": "user", "content": message.text},
        {"role": "assistant", "content": message.text}],
        temperature=0.2,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)

    bot.reply_to(message, text=response['choices'][0]['message']['content'])


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except (telebot.apihelper.ApiException, ConnectionError) as e:
            logger.error(e)
            time.sleep(5)
            continue
