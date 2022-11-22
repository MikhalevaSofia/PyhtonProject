from threading import Semaphore
from telebot import types
from threading import Thread
import pandas as pd
import telebot
import calculations
import users
import time
import schedule
import pathlib
import os

tikers_semaphore = Semaphore(value=1)
dir_figure = './resources/Figure/'
token = '5576162699:AAEzBKzcfy-Eq4Vk4DinKZL9tFMWlIMBs6g'
bot = telebot.TeleBot(token)
df = pd.DataFrame()

print('Я работаю!')
markupStart = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('Тикеры MOEX/Tikers of MOEX'),
    types.KeyboardButton('Информация обо мне/Information about me'),
    types.KeyboardButton('Анекдот (опция только на русском)'),
    types.KeyboardButton('Мои тикеры MOEX/My MOEX tikers')
)
markupTikers = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('AFLT'),
    types.KeyboardButton('SBER'),
    types.KeyboardButton('GAZP'),
    types.KeyboardButton('VTBR'),
    types.KeyboardButton('ROSN'),
    types.KeyboardButton('Другое/Other'),
    types.KeyboardButton('Назад/Back')
)
markupBack = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('Назад/Back')
)
markupAdd = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('Добавить тикер/Add tiker'),
    types.KeyboardButton('Назад/Back')
)
markupRemove = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('Удалить тикер/Remove tiker'),
    types.KeyboardButton('Назад/Back')
)




@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user), reply_markup=markupStart)
    bot.send_message(message.chat.id,
                     'Меня зовут Traider`s Assistant. Я твой бот-помощник в осуществлении торгов на Московской бирже. Для получения информации ты можешь воcпользоваться подсказками ниже.')

    bot.send_message(message.chat.id, 'Hey, {0.first_name}! '.format(message.from_user))
    bot.send_message(message.chat.id,
                     'My name`s Traider`s Assistant. I`m your bot assistant in traiding on the MOEX. If you need more information, you can use the tips below.'
                     )




@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Тикеры MOEX/Tikers of MOEX':

            bot.send_message(message.chat.id, 'Тикеры MOEX/Tikers of MOEX', reply_markup=markupTikers)
        elif message.text == 'Информация обо мне/Information about me':

            bot.send_message(message.chat.id, 'Информация обо мне/Information about me')
            bot.send_message(message.chat.id,
                             'Как я уже сказал, я буду помогать тебе торговать на московской бирже: покажу тебе изменение котировок, расскажу, когда лучше купить/продать твои акции, а также построю графики инструментов технического анализа, которые помогут тебе распознать достоверность отправленного мной сигнала')
            bot.send_message(message.chat.id,
                             'As I said, I will help you trade on the MOEX: I will show you the change in quotations, tell you when it is better to buy/ sell your shares, and also build graphs of technical analysis tools that will help you recognize the reliability of the signal I sent',
                             reply_markup=markupBack)
        elif message.text == 'Анекдот (опция только на русском)':
            bot.send_message(message.chat.id, 'Анекдот (опция только на русском)')
            bot.send_message(message.chat.id, 'Беседуют две блондинки:'
                                              '— Как ты могла при всех назвать меня дурой?'
                                              '— Извини, ты же не предупредила, что скрываешь.',
                             reply_markup=markupBack)
        elif message.text == 'Назад/Back':
            bot.send_message(message.chat.id, 'Назад/Back', reply_markup=markupStart)
        elif message.text == 'Другое/Other':
            bot.send_message(message.chat.id, 'Введи название тикера')
        elif message.text == 'Мои тикеры MOEX/My MOEX tikers':
            tikers_semaphore.acquire(blocking=True, timeout=0.5)
            if users.get_user_tikers(message.chat.id) == '':
                bot.send_message(message.chat.id, 'У тебя ещё нет тикеров!/ You do not have tikers yet',
                                 reply_markup=markupAdd)
            else:
                bot.send_message(message.chat.id, users.get_user_tikers(message.chat.id),
                                 reply_markup=markupRemove)

            tikers_semaphore.release()
        elif message.text == 'Добавить тикер/Add tiker':
            bot.send_message(message.chat.id, 'Тикеры MOEX/Tikers of MOEX', reply_markup=markupTikers)
        elif message.text == 'Удалить тикер/Remove tiker':
            bot.send_message(message.chat.id, 'Введи название тикера, который необходимо удалить',
                             reply_markup=markupBack)





        else:
            if calculations.check_tiker(message.text):
                tikers_semaphore.acquire(blocking=True, timeout=0.5)
                users.add_user_tiker(message.from_user.id, message.text)
                tikers_semaphore.release()


def job():
    for file in os.listdir(dir_figure):
        if file.endswith('.png'):
            os.remove(os.path.join(dir_figure, file))
    print(f'Clear directory {dir_figure}')
    for row in users.users_df.itertuples():
        for tiker in row.tikers.split(','):
            print(calculations.get_calculation(tiker))
            send_pictures_to_users(row.id, tiker)

    print('Finish calculations')


schedule.every().day.at('19:03').do(job)


# schedule.every().seconds.do(job)


def sched():
    while True:
        schedule.run_pending()
        time.sleep(1)


thread = Thread(target=sched)
thread.start()


def send_pictures_to_users(id: int, tiker: str):
    bot.send_message(id, tiker)
    for file in os.listdir(dir_figure):
        if file.startswith(tiker):
            bot.send_photo(id, photo=open(f'{dir_figure}{file}', 'rb'))


bot.polling(none_stop=True)
