import telebot
from telebot import types
token = '5576162699:AAEzBKzcfy-Eq4Vk4DinKZL9tFMWlIMBs6g'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	button1 = types.KeyboardButton('Тикеры MOEX/Tikers of MOEX')
	button2 = types.KeyboardButton('Информация обо мне/Information about me')
	button3 = types.KeyboardButton('Анекдот (опция только на русском)')

	markup.add(button1, button2, button3)
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

@bot.message_handler(content_types=['text'])
def bot_message(message):
	if message.chat.type == 'private':
		if message.text == 'Тикеры MOEX/Tikers of MOEX':
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton('AFLT')
			button2 = types.KeyboardButton('SBER')
			button3 = types.KeyboardButton('GAZP')
			button4 = types.KeyboardButton('VTBR')
			button5 = types.KeyboardButton('ROSN')
			button6 = types.KeyboardButton('Другое/Other')
			button7 = types.KeyboardButton('Назад/Back')
			markup.add(button1, button2, button3, button4, button5, button6, button7)
			bot.send_message(message.chat.id, 'Тикеры MOEX/Tikers of MOEX', reply_markup=markup)
		elif message.text == 'Информация обо мне/Information about me':
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton('Назад/Back')
			markup.add(button1)
			bot.send_message(message.chat.id, 'Информация обо мне/Information about me')
			bot.send_message(message.chat.id,
							 'Как я уже сказал, я буду помогать тебе торговать на московской бирже: покажу тебе изменение котировок, расскажу, когда лучше купить/продать твои акции, а также построю графики инструментов технического анализа, которые помогут тебе распознать достоверность отправленного мной сигнала')
			bot.send_message(message.chat.id,
							 'As I said, I will help you trade on the MOEX: I will show you the change in quotations, tell you when it is better to buy/ sell your shares, and also build graphs of technical analysis tools that will help you recognize the reliability of the signal I sent',
							 reply_markup=markup)



		elif message.text == 'Анекдот (опция только на русском)':
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton('Назад/Back')
			markup.add(button1)
			bot.send_message(message.chat.id, 'Анекдот (опция только на русском)')
			bot.send_message(message.chat.id, 'Беседуют две блондинки:'
											  '— Как ты смогла при всех назвать меня дурой?'
											  '— Извини, ты же не предупредила, что скрываешь.', reply_markup=markup)

		elif message.text == 'Назад/Back':
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton('Тикеры MOEX/Tikers of MOEX')
			button2 = types.KeyboardButton('Информация обо мне/Information about me')
			button3 = types.KeyboardButton('Анекдот (опция только на русском)')

			markup.add(button1, button2, button3)
			bot.send_message(message.chat.id, 'Назад/Back', reply_markup=markup)


bot.polling(none_stop=True)
