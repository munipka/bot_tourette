import time
import telebot
from telebot import util
from telebot import types
from DBcm import UseDatabase
from itertools import chain
from random import randint

bot = telebot.TeleBot('5333141001:AAHb7nhVtJpJ5YLjI1T6sz2qxUHJd4_U2vQ');

dbconfig = {'host':'127.0.0.1',
             'user': 'mnep',
             'password': 'r992mma772nm',
             'database': 'telegram_bots',}

nice_words = ['лучший','красавчик','гений', 'неповторимый', 'умный', 'Бог', 'Апполон', 'уникальный', 'охуенный']


hellomsg = 'Привет, {user_name}! \n'
hellomsg += 'Если вы хотите обозвать вашего собеседника не очень приятным, но рандомным словом, '
hellomsg += 'то введите @swearings_bot в чате с ним и нажмите кнопку "Рандомное ругательство".'

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    message = bot.send_message(message.from_user.id, hellomsg.format(
                                 user_name=message.from_user.first_name))

def show_swearing(query):
    try:
        num = randint(1,186)
        with UseDatabase(dbconfig) as cursor:
            _SQL = """SELECT word FROM Swear
                    WHERE num={num}"""
            cursor.execute(_SQL.format(num=num))
            content = cursor.fetchall()
            results=''
            for item in content:
                results+='Ты - '+ item[0].lower()
            return results
    except Exception as e:
        print(e)

def show_nice(query):
    try:
        num = randint(0,2)
        result = 'Ты - ' + nice_words[num]
        return result
    except Exception as e:
        print(e)
        

@bot.inline_handler(func=lambda query: len(query.query) == 0)
def empty_query(query):
    try:
        if query.from_user.id == 853566094:
            msg = show_nice(query)
        else:
            msg=show_swearing(query)
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
        bot.answer_inline_query(query.id, [r,r2], cache_time=0, is_personal=True)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)