import os

import telebot
from crawler.brasileiro_a import last_results
from dotenv import find_dotenv, load_dotenv

dot_env = find_dotenv()
load_dotenv(dot_env)
BOT_TOKEN = os.getenv('BOT_API')

bot = telebot.TeleBot(str(BOT_TOKEN))


@bot.message_handler(commands=['ultimos_resultados'])
def show_last_matches_results(message):
    """Shows the last matches results of brasileirão divison A."""
    CHAT_ID = message.chat.id
    array_matches_results = last_results()
    string_matches_results = ''
    for results in array_matches_results:
        string_matches_results += results
    bot.send_message(CHAT_ID, string_matches_results)


@bot.message_handler(commands=['start'])
def start_message(message):
    """Shows the user guide message and the keyboard buttons."""
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    keyboard.row('/ultimos_resultados')
    user_guide_message = """
    Bem vindo ao Fute Bot !
Escreva ou aperte um dos botões que aparecem no seu teclado. \n
Caso tenha alguma dificuldade, digite ou aperte "/help" para ver
a lista de comandos disponiveis.
    """
    bot.send_message(
        message.chat.id, user_guide_message, reply_markup=keyboard
    )


bot.polling()
