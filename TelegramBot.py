import telebot
from telebot import types
token = '5576162699:AAEzBKzcfy-Eq4Vk4DinKZL9tFMWlIMBs6g'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	button1 = types.KeyboardButton('Тикеры MOEX/Tikers of MOEX')
	button2 = types.KeyboardButton('Информация обо мне/Information about me')

	markup.add(button1, button2)
	bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user))
	bot.send_message(message.chat.id,
					 'Меня зовут Traider`s Assistant. Я твой бот-помощник в осуществлении торгов на Московской бирже. Для получения информации ты можешь воcпользоваться подсказками ниже.')

	bot.send_message(message.chat.id, 'Hey, {0.first_name}! '.format(message.from_user))
	bot.send_message(message.chat.id,
					 'My name`s Traider`s Assistant. I`m your bot assistant in traiding on the MOEX. If you need more information, you can use the tips below.',
					 reply_markup=markup)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)
#     bot.send_message(chat_id=message.chat.id, text="Сигнал")


bot.polling(none_stop=True)
