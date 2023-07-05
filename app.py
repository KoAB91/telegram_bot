import telebot

from config import TOKEN
from extensions import ConversionException, CurrenciesConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    answer = 'Чтобы начать работу введите команду боту в следующем формате (через пробел):' \
             '\n<буквенный код валюты для конвертации>\n<буквенный код валюты, в которую осуществляется конвертация>' \
             '\n<сумма (по умолчанию равняется 1 единице)>. ' \
             '\nДля того, чтобы узнать доступные для конвертации валюты и их коды, введите команду /values'
    bot.reply_to(message, answer)


@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    answer = 'Для конвертации необходимо ввести команду в следующем формате (через пробел):' \
             '\n<буквенный код валюты для конвертации>\n<буквенный код валюты, в которую осуществляется конвертация>' \
             '\n<сумма (по умолчанию равняется 1 единице)>\nПример ввода: USD RUB 100\n ' \
             'Для того, чтобы узнать доступные для конвертации валюты и их коды, введите команду /values'
    bot.reply_to(message, answer)


@bot.message_handler(commands=['values'])
def get_values(message: telebot.types.Message):
    answer = CurrenciesConverter.show_currencies()
    bot.reply_to(message, answer)


@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        currency_price = CurrenciesConverter.get_price(values)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e} ')
    else:
        bot.send_message(message.chat.id, currency_price)


bot.polling()
