import telebot
from config import currency, TOKEN
from utils import ConversationException, Converter

bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Введите запрос в формате: \
    <исходная валюта> <желаемая валюта> <количество> \
    \n Увидеть доступные валюты: /values")

@bot.message_handler(commands=['values'])
def value(message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text = text + '\n' + key
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        message.text = message.text.lower()
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConversationException('неправильное количество аргументов')
        in_currency, out_currency, amount = values
        total = Converter.convert(in_currency, out_currency, amount)
    except ConversationException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя: {e}')

    except Exception as e:
        bot.send_message(message.chat.id, f'Системная ошибка:'
                                          f''
                                          f''
                                          f' {e}')
    else:
        bot.send_message(message.chat.id, f'{total} {out_currency}')

bot.polling(none_stop=True)



