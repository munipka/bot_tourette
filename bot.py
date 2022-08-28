import time
import telebot
from telebot import types

from database import get_word

from random import randint
import config

bot = telebot.TeleBot(config.BOT_TOKEN)

hellomsg = 'Привет, {user_name}! \n'
hellomsg += 'Если вы хотите обозвать вашего собеседника не очень приятным, но рандомным словом, '
hellomsg += 'то введите @swearings_bot в чате с ним и нажмите кнопку "Рандомное ругательство".'

help_msg = """Если вы хотите обозвать вашего собеседника не очень приятным, но рандомным словом, то введите
@swearings_bot в чате с ним и нажмите кнопку "Рандомное ругательство".
Помимо этого, можно ввести имя или маленькую фразу после 
"@swearings_bot".
Если после последнего слова вставить следующие символы, то они изменят шаблон:
,(запятая) - отмена тире, но сохранение запятой,
:(двоеточие) - 3 веселых слова, 
.(точка) - никаких знаков"""


action_icon = 'https://i.ibb.co/4VVMcpc/442-4427964-its-a-logo-of-swearing-male-reduced-to.png'
help_icon = 'https://i.ibb.co/sWQQKbb/help.png'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, hellomsg.format(
        user_name=message.from_user.first_name))


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, help_msg)


def show_swearing():
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
        if query.query[-1:] == ',':
            for item in content:
                results += f'{query.query} ' + item[0].lower()
        elif query.query[-1:] == ':':
            content = []
            for i in range(3):
                num = randint(1, 272)
                content.append(get_word(num))
            results = f'{query.query[:-1]} \- ' + content[0][0][0][:-1].lower() + ', '
            results += content[1][0][0][:-1].lower() + ' и ' + content[2][0][0][:-1].lower()
        elif query.query[-1:] == '.':
            for item in content:
                results += f'{query.query[:-1]} ' + item[0].lower()
        else:
            for item in content:
                results += f'{query.query} \- ' + item[0].lower()
        return results
    except Exception as e:
        print(e)


@bot.inline_handler(func=lambda query: len(query.query) == 0)
def empty_query(query):
    try:
        msg = show_swearing()
        r = types.InlineQueryResultArticle(
            id='1',
            title="Рандомное ругательство",
            description='Обзовите вашего собеседника',
            input_message_content=types.InputTextMessageContent(
                message_text=msg),
            thumb_url=action_icon,
            thumb_width=48, thumb_height=48
        )
        r2 = types.InlineQueryResultArticle(
            id='2',
            title='Помощь',
            input_message_content=types.InputTextMessageContent(
                message_text=help_msg),
            thumb_url=help_icon,
            thumb_width=48, thumb_height=48
        )
        bot.answer_inline_query(query.id, [r, r2], cache_time=0, is_personal=True)
    except Exception as e:
        print(e)


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def not_empty_query(query):
    try:
        msg = show_swearing_extra(query)
        name_eng = query.query
        try:
            r = types.InlineQueryResultArticle(
                id='1',
                title=f"Закончить фразу",
                description='Обзовите этого человека',
                input_message_content=types.InputTextMessageContent(
                    message_text=msg.replace(".", "\\."),
                    parse_mode="MarkdownV2"
                ))
        except:
            r = types.InlineQueryResultArticle(
                id='1',
                title=f"Обругать {name_eng}",
                description='Обзовите этого человека',
                input_message_content=types.InputTextMessageContent(
                    message_text=msg.replace(".", "\\."),
                    parse_mode="MarkdownV2"
                ))
        help_button = types.InlineQueryResultArticle(
            id='2',
            title='Помощь',
            input_message_content=types.InputTextMessageContent(
                message_text=help_msg),
        )
        bot.answer_inline_query(query.id, [r, help_button], cache_time=0, is_personal=True)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)
