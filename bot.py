import time
import telebot
from telebot import types

from database import get_word

from random import randint
import pymorphy2
import config

bot = telebot.TeleBot(config.BOT_TOKEN)


hellomsg = 'Привет, {user_name}! \n'
hellomsg += 'Если вы хотите обозвать вашего собеседника не очень приятным, но рандомным словом, '
hellomsg += 'то введите @swearings_bot в чате с ним и нажмите кнопку "Рандомное ругательство".'


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    message = bot.send_message(message.from_user.id, hellomsg.format(
        user_name=message.from_user.first_name))


def show_swearing(query):
    try:
        num = randint(1, 272)
        content = get_word(num)
        results = ''
        for item in content:
            results += 'Ты - ' + item[0].lower()
        return results
    except Exception as e:
        print(e)


def show_swearing_extra(query):
    try:
        num = randint(1, 272)
        content = get_word(num)
        results = ''
        for item in content:
            results += f'{query.query} \- ' + item[0].lower()
        return results
    except Exception as e:
        print(e)


@bot.inline_handler(func=lambda query: len(query.query) == 0)
def empty_query(query):
    try:
        msg = show_swearing(query)
        r = types.InlineQueryResultArticle(
            id='1',
            title="Рандомное ругательство",
            description='Обзовите вашего собеседника',
            input_message_content=types.InputTextMessageContent(
                message_text=msg,
            )

        )
        r2 = types.InlineQueryResultArticle(
            id='2',
            title='Помощь',
            input_message_content=types.InputTextMessageContent(
                message_text=
                'В любом чате напишите @swearings_bot и нажмите на кнопку "Рандомное ругательство"'),
        )
        bot.answer_inline_query(query.id, [r, r2], cache_time=0, is_personal=True)
    except Exception as e:
        print(e)


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def not_empty_query(query):
    try:
        msg = show_swearing_extra(query)
        morph = pymorphy2.MorphAnalyzer()
        name = morph.parse(query.query)[0]
        gent = name.inflect({'accs'})
        r = types.InlineQueryResultArticle(
            id='1',
            title=f"Обругать {str.capitalize(gent.word)}",
            description='Обзовите этого человека',
            input_message_content=types.InputTextMessageContent(
                message_text=msg.replace(".", "\\."),
                parse_mode="MarkdownV2"
            )

        )
        r2 = types.InlineQueryResultArticle(
            id='2',
            title='Помощь',
            input_message_content=types.InputTextMessageContent(
                message_text=
                'В любом чате напишите @wallets_list_bot, введите имя кошелька и нажмите, чтобы отправить его'),
        )
        bot.answer_inline_query(query.id, [r, r2], cache_time=0, is_personal=True,
                                switch_pm_text='Добавить новый',
                                switch_pm_parameter='add')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)
