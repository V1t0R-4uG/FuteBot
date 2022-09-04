import os
from time import sleep
import datetime

import telebot
from crawler.Brazil_Championships import brasileiro_a
from dotenv import find_dotenv, load_dotenv

dot_env = find_dotenv()
load_dotenv(dot_env)
BOT_TOKEN = os.getenv('BOT_API')

bot = telebot.TeleBot(str(BOT_TOKEN))


@bot.message_handler(commands=['ultimos_resultados_BRA'])
def show_last_matches_results_BRA(message):
    """Shows the last matches results of brasileirão divison A."""
    CHAT_ID = message.chat.id
    array_matches_results = brasileiro_a.last_results()
    string_matches_results = ''
    for results in array_matches_results:
        string_matches_results += results
    bot.send_message(CHAT_ID, string_matches_results)


@bot.message_handler(commands=['tabela_BRA'])
def show_table_BRA(message):
    """show table of brasileirão divison A"""
    CHAT_ID = message.chat.id
    table_array = brasileiro_a.table()
    string_table = """"""
    for team in table_array:
        name = team['team_name']
        position = team['team_position']
        wins = team['team_wins']
        loss = team['team_losses']
        draws = team['team_draws']
        points = team['team_points']
        to_append = (
            f'\n{position}° {name} \n P: {points} '
            f' V: {wins}  E: {draws}  D: {loss} \n'
        )
        string_table += to_append
    bot.send_message(CHAT_ID, string_table)


@bot.message_handler(commands=['resumo_time_BRA'])
def ask_team_name(message):
    """Ask the user what team him want to see."""
    CHAT_ID = message.chat.id
    message = """🤖 Digite sem acento o nome do time que você deseja ver."""
    team_name = bot.send_message(CHAT_ID, message)
    bot.register_next_step_handler(team_name, show_club_overview)


def show_club_overview(message):
    """Show the team overview that the user request and ask if the user
    want to see more information."""
    CHAT_ID = message.chat.id
    TEAM_NAME = message.text
    try:
        TEAM_OVERVIEW = brasileiro_a.team_overview(TEAM_NAME)
        TEAM_IMAGE = TEAM_OVERVIEW['teamImage']
        team_info = f"""\
⚽ Nome: {TEAM_OVERVIEW['team_fullname']}
🎯 Técnico: {TEAM_OVERVIEW['manager']}
🏟️ Estádio: {TEAM_OVERVIEW['stadium']}
📍 Cidade: {TEAM_OVERVIEW['city']}
⚽ Gols Marcados: {TEAM_OVERVIEW['goalsScored']}
😡 Gols Sofridos: {TEAM_OVERVIEW['goalsConceded']}
🟨 Cartões Amarelos: {TEAM_OVERVIEW['yellowCards']}
🟥 Cartões Vermelhos: {TEAM_OVERVIEW['redCards']}
        """
        button1 = telebot.types.InlineKeyboardButton(
            text='ver estatisticas', callback_data=f'{TEAM_NAME}'
        )
        button2 = telebot.types.InlineKeyboardButton(
            text='sair', callback_data='sair'
        )
        keyboard_inline = telebot.types.InlineKeyboardMarkup().add(
            button1, button2
        )
        bot.send_sticker(CHAT_ID, TEAM_IMAGE)
        bot.send_message(CHAT_ID, team_info, reply_markup=keyboard_inline)
    except:
        error_message = """
    ❌ Erro ao trazer informações do time, certifique-se que você digitou\
 corretamente e sem acento. ❌
        """
        bot.send_message(CHAT_ID, error_message)


@bot.callback_query_handler(func=lambda call: True)
def show_statistics_or_exit(call):
    """Show user the team statistics if he wants to."""
    user_answer = call.data
    if user_answer != 'sair':
        reply_message = 'Carregando estatisticas'
        bot.answer_callback_query(
            callback_query_id=call.id, text=reply_message
        )
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id
        )
        statistics = brasileiro_a.team_statistics(user_answer)
        statistics_string = f"""
Numero de partidas jogadas: {statistics['matches']}
Gols Marcados: {statistics['goalsScored']}
Gols Sofridos: {statistics['goalsConceded']}
Chutes: {statistics['shots']}
Gols de Penalti: {statistics['penaltyGoals']}
Gols de Falta: {statistics['freeKickGoals']}
Chutes de Falta: {statistics['freeKickShots']}
Gols dentro da área: {statistics['goalsFromInsideTheBox']}
Gols de fora da área: {statistics['goalsFromOutsideTheBox']}
Chutes dentro da área: {statistics['shotsFromInsideTheBox']}
Chutes de fora da área: {statistics['shotsFromOutsideTheBox']}
Gols de cabeça: {statistics['headedGoals']}
Gols com a perna esquerda: {statistics['leftFootGoals']}
Gols com a perna direita: {statistics['rightFootGoals']}
Grandes chances criadas: {statistics['bigChancesCreated']}
Grandes chances perdidas: {statistics['bigChancesMissed']}
Chutes no gol: {statistics['shotsOnTarget']}
Chutes fora do gol: {statistics['shotsOffTarget']}
Chutes na trave: {statistics['hitWoodwork']}
Dribles bem sucedidos: {statistics['successfulDribbles']}
Tentativas de dribles: {statistics['dribbleAttempts']}
Escanteios: {statistics['corners']}
Média de posse de bola: {statistics['averageBallPossession']:.2f}%
Total de passes: {statistics['totalPasses']}
Passes precisos: {statistics['accuratePasses']}
passes precisos: {statistics['accuratePassesPercentage']:.2f}%
Total de bolas longas: {statistics['totalLongBalls']}
Bolas longas precisas: {statistics['accurateLongBalls']}
Bolas longas precisas: {statistics['accurateLongBallsPercentage']:.2f}%
Total de cruzamentos: {statistics['totalCrosses']}
Cruzamentos precisos: {statistics['accurateCrosses']}
cruzamentos precisos: {statistics['accurateCrossesPercentage']:.2f}%
Jogos sem sofrer gols: {statistics['cleanSheets']}
Total de desarmes: {statistics['tackles']}
Intercepções: {statistics['interceptions']}
Total de duelos: {statistics['totalDuels']}
Total de duelos ganhos: {statistics['duelsWon']}
Total de duelos áereos: {statistics['totalAerialDuels']}
Faltas: {statistics['fouls']}
Cartões amarelos: {statistics['yellowCards']}
Cartões vermelhos: {statistics['redCards']}
"""
        bot.send_message(call.message.chat.id, text=statistics_string)
    else:
        reply_message = 'ok, saindo...'
        bot.answer_callback_query(
            callback_query_id=call.id, text=reply_message
        )
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id
        )
        return


@bot.message_handler(commands=['confrontos_por_rodada_BRA'])
def ask_user_the_round_number(message):
    CHAT_ID = message.chat.id
    message = """🤖 Digite o número da rodada que você deseja ver."""
    round_number = bot.send_message(CHAT_ID, message)
    bot.register_next_step_handler(round_number, show_matches_by_round_number)


def show_matches_by_round_number(message):
    CHAT_ID = message.chat.id
    passed_round_number = message.text
    round_number_is_less_than_limit = int(passed_round_number) < 39
    roud_number_is_actualy_number = passed_round_number.isnumeric()
    a_round = round_number_is_less_than_limit and roud_number_is_actualy_number
    if not a_round:
        bot.send_message(CHAT_ID, '❌ Erro, digite um número válido ❌')
        return
    matches = brasileiro_a.show_matches_by_round_number(passed_round_number)
    string_of_matches_pretify = """"""
    for match in matches:
        home_team = match['home_team']
        away_team = match['away_team']
        home_score = match['home_score']
        away_score = match['away_score']
        time_stamp = match['time_stamp']

        the_match_will_happen = home_score ==  {}
        the_match_is_happening_now = 'normaltime' not in home_score

        if the_match_will_happen:
            append_future_match = f"""\n🔸A Jogar:\n{home_team} X {away_team}\
 - \n🗓️ {time_stamp}\n"""
            string_of_matches_pretify += append_future_match

        elif the_match_is_happening_now:
            match_happening_now = f"""\n🔁 Em andamento:
{home_team} \
{home_score['display']} X {away_score['display']} {away_team} \n"""
            string_of_matches_pretify += match_happening_now

        else:
            ended_match = f"""\n🔹Encerrado:
{home_team} {home_score['display']} X \
{away_score['display']} {away_team} - \n🗓️ {time_stamp}\n"""
            string_of_matches_pretify += ended_match

    bot.send_message(
        CHAT_ID, f'Carregando confrontos da rodada {passed_round_number}...'
    )
    sleep(1)
    bot.send_message(CHAT_ID, string_of_matches_pretify)


@bot.message_handler(commands=['help', 'ajuda'])
def help_command(message):
    """Send the bot User Guide to the user."""
    CHAT_ID = message.chat.id
    string = """
Lista de comandos disponiveis: \n
/ultimos_resultados_BRA : ultimos resultados do brasileirão A.
/tabela_BRA : tabela do brasileirão A.
/resumo_time_BRA : Overview e estatisticas de qualquer clube do brasileirão
/confrontos_por_rodada_BRA : Confrontos que aconteceram ou irão acontecer
    """
    bot.send_message(CHAT_ID, string)


@bot.message_handler(commands=['start'])
def start_message(message):
    """Shows the user guide message and the keyboard buttons."""
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    keyboard.row('/ultimos_resultados_BRA')
    keyboard.row('/tabela_BRA')
    keyboard.row('/resumo_time_BRA')
    keyboard.row('/confrontos_por_rodada_BRA')
    user_guide_message = """
    Bem vindo ao Fute Bot ⚽️ ! \n
Escreva ou aperte um dos botões que aparecem no seu teclado. \
Caso tenha alguma dificuldade, digite ou aperte "/help" "/ajuda" para ver \
a lista de comandos disponiveis.
Os comandos com o sufixo 'BRA' correspondem ao brasileirão série A.
    """
    bot.send_message(
        message.chat.id, user_guide_message, reply_markup=keyboard
    )


bot.polling()
