import os
from time import sleep

import telebot
from crawler.Brazil_Championships.brasileiro_a import last_results, table
from dotenv import find_dotenv, load_dotenv

dot_env = find_dotenv()
load_dotenv(dot_env)
BOT_TOKEN = os.getenv('BOT_API')

bot = telebot.TeleBot(str(BOT_TOKEN))


@bot.message_handler(commands=['ultimos_resultados_BRA'])
def show_last_matches_results_BRA(message):
    """Shows the last matches results of brasileirão divison A."""
    CHAT_ID = message.chat.id
    array_matches_results = last_results()
    string_matches_results = ''
    for results in array_matches_results:
        string_matches_results += results
    bot.send_message(CHAT_ID, 'Carregando ultimos resultados...')
    sleep(1)
    bot.send_message(CHAT_ID, string_matches_results)


@bot.message_handler(commands=['tabela_BRA'])
def show_table_BRA(message):
    """show table of brasileirão divison A"""
    CHAT_ID = message.chat.id
    table_array = table()
    string_table = """\n Pontos: 🅿️ 
    Vitórias:   🟢
    Derrotas:  🔴
    Empates:  ❌ \n"""
    for team in table_array:
        name = team['team_name']
        position = team['team_position']
        wins = team['team_wins']
        loss = team['team_losses']
        draws = team['team_draws']
        points = team['team_points']
        to_append = (
            f'\n{position}° {name} \n 🅿️ {points} '
            f' 🟢{wins}  ❌{draws}  🔴{loss} \n'
        )
        string_table += to_append
    bot.send_message(CHAT_ID, string_table)


@bot.message_handler(commands=['help', 'ajuda'])
def help_command(message):
    """Send the bot User Guide to the user."""
    CHAT_ID = message.chat.id
    string = """
Lista de comandos disponiveis: \n
/ultimos_resultados_BRA : ultimos resultados do brasileirão A. \n
/tabela_BRA : tabela do brasileirão A.
    """
    bot.send_message(CHAT_ID, string)


@bot.message_handler(commands=['start'])
def start_message(message):
    """Shows the user guide message and the keyboard buttons."""
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    keyboard.row('/ultimos_resultados_BRA', '/tabela_BRA')
    user_guide_message = """
    Bem vindo ao Fute Bot ⚽️ ! \n
Escreva ou aperte um dos botões que aparecem no seu teclado. \
Caso tenha alguma dificuldade, digite ou aperte "/help" "/ajuda" para ver \
a lista de comandos disponiveis.
    """
    bot.send_message(
        message.chat.id, user_guide_message, reply_markup=keyboard
    )


bot.polling()
