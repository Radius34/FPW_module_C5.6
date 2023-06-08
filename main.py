import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Привет! Я бот, который может помочь тебе узнать цену на определенное количество валюты.'\
           '\n Для этого напиши мне сообщение в формате: '\
           '\n <валюта, цену которой ты хочешь узнать>' \
           ' <валюта, в которую ты хочешь перевести>' \
           ' <количество первой валюты>'\
           '\n Например: USD RUB 100  '\
           '\n Для получения списка доступных валют напиши мне команду /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n {e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n {e}")
    else:
        bot.reply_to(message, answer)

bot.polling()
