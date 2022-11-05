import datetime
import os
from time import sleep

import telebot
from crawler.Brazil_Championships import brasileiro_a
from dotenv import find_dotenv, load_dotenv

dot_env = find_dotenv()
load_dotenv(dot_env)
BOT_TOKEN = os.getenv('BOT_API')

bot = telebot.TeleBot(str(BOT_TOKEN))


@bot.message_handler(commands=['tabela_bra'])
def show_table_BRA(message):
    """show table of brasileirão divison A"""
    CHAT_ID = message.chat.id
    raw_table_info = brasileiro_a.table()
    if raw_table_info['message'] == 'error':
        bot.send_message(CHAT_ID, 'Erro ao trazer a tabela.')
        return
    teams = raw_table_info['value']
    string = str()
    for team in teams:
        if int(team.position) > 16:
            s = (
                f'\n🅱 {team.position}° {team.name} - P: {team.points}\n'
            )
        else:
            s = (
                f'\n{team.position}° {team.name}  -  P: {team.points}\n'
            )
        string = string + s
    bot.send_message(CHAT_ID, string)


@bot.message_handler(commands=['resumo_time_bra'])
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
        team_info = (
            f"⚽ Nome: {TEAM_OVERVIEW['team_fullname']}\n"
            f"🎯 Técnico: {TEAM_OVERVIEW['manager']}\n"
            f"🏟️ Estádio: {TEAM_OVERVIEW['stadium']}\n"
            f"📍 Cidade: {TEAM_OVERVIEW['city']}\n"
            f"⚽ Gols Marcados: {TEAM_OVERVIEW['goalsScored']}\n"
            f"😡 Gols Sofridos: {TEAM_OVERVIEW['goalsConceded']}\n"
            f"🟨 Cartões Amarelos: {TEAM_OVERVIEW['yellowCards']}\n"
            f"🟥 Cartões Vermelhos: {TEAM_OVERVIEW['redCards']}\n"
        )
        #button1 = telebot.types.InlineKeyboardButton(
        #    text='ver estatisticas', callback_data=f'ver estatisticas:{TEAM_NAME}'
        #)
        #keyboard_inline = telebot.types.InlineKeyboardMarkup().add(button1)
        bot.send_sticker(CHAT_ID, TEAM_IMAGE)
        bot.send_message(CHAT_ID, team_info)
    except:
        error_message = (
            f'❌ Erro ao trazer informações do time, '
            f'certifique-se que você digitou corretamente e sem acento. ❌'
        )
        bot.send_message(CHAT_ID, error_message)


@bot.message_handler(commands=['confrontos_por_rodada_bra'])
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

        the_match_will_happen = home_score == {}
        the_match_is_happening_now = 'normaltime' not in home_score

        if the_match_will_happen:
            append_future_match = (
                f'\n🔸A Jogar: \n {home_team} X {away_team} -'
                f'\n🗓️ {time_stamp}\n'
            )
            string_of_matches_pretify += append_future_match

        elif the_match_is_happening_now:
            match_happening_now = (
                f'\n🔁 Em andamento: \n'
                f'{home_team} '
                f"{home_score['display']} X {away_score['display']} "
                f'{away_team} \n'
            )
            string_of_matches_pretify += match_happening_now

        else:
            ended_match = (
                f'\n🔹Encerrado: \n'
                f"{home_team} {home_score['display']} X "
                f"{away_score['display']} {away_team} - \n🗓️ {time_stamp}\n"
            )
            string_of_matches_pretify += ended_match

    bot.send_message(
        CHAT_ID, f'Carregando confrontos da rodada {passed_round_number}...'
    )
    sleep(1)
    bot.send_message(CHAT_ID, string_of_matches_pretify)


@bot.message_handler(commands=['jogador_por_time_bra'])
def ask_team_and_player_name(message):
    """Ask the user what team and player him want to see."""
    CHAT_ID = message.chat.id
    message = (
        f'Digite sem acentos o nome do time e o nome do jogador separados '
        f'por virgula. Exemplo: \n'
        f'atletico mineiro, guilherme arana'
    )
    team_name = bot.send_message(CHAT_ID, message)
    bot.register_next_step_handler(team_name, player_overview)


def player_overview(message):
    CHAT_ID = message.chat.id
    split_message = message.text.split(',')
    team_name = split_message[0]
    player_name = split_message[1].lstrip()
    overview = brasileiro_a.return_player_overview(team_name, player_name)
    if type(overview) == ValueError:
        bot.send_message(CHAT_ID, 'O jogador informado não foi encontrado!')
        return
    player_id = overview['player']['id']
    player_image = brasileiro_a.return_player_photo(player_id)
    preferred_foot = {'Left': 'Esquerdo', 'Right': 'Direito'}
    contract_time = datetime.datetime.fromtimestamp(
        overview['player']['contractUntilTimestamp']
    )
    preferred_foot = preferred_foot[overview['player']['preferredFoot']]
    market_value = overview['player']['proposedMarketValueRaw']['value']
    message_with_player_atributes = (
        f"⚽ Nome: {overview['player']['name']}\n"
        f"👕 Número da camisa: {overview['player']['jerseyNumber']}\n"
        f"🙋 Altura: {overview['player']['height']}\n"
        f'👟 Pé de preferencia: {preferred_foot}\n'
        f"🏳️País de origem: {overview['player']['country']['name']}\n"
        f'📆 Fim do contrato: '
        f'{contract_time}\n'
        f'💰 Valor de mercado: EUR {market_value}\n',
        f'estatisticas, {player_name}, {team_name}',
    )
    button1 = telebot.types.InlineKeyboardButton(
        text='ver estatisticas completas',
        callback_data=message_with_player_atributes[1],
    )
    keyboard_inline = telebot.types.InlineKeyboardMarkup().add(button1)
    bot.send_sticker(CHAT_ID, player_image)
    bot.send_message(
        CHAT_ID, message_with_player_atributes[0], reply_markup=keyboard_inline
    )


@bot.callback_query_handler(func=lambda call: 'estatisticas' in call.data)
def show_player_statistics_or_exit(call):
    """Show user the player statistics if he wants to."""
    response_callback = call.data.split(',')
    team_name = response_callback[2].lstrip()
    player_name = response_callback[1].lstrip()
    overall = brasileiro_a.return_player_overall(team_name, player_name)
    statistics = overall['statistics']
    overall_message = (
        f"Gols: {statistics['goals']}\n"
        f"Grandes chances criadas: {statistics['bigChancesCreated']}\n"
        f"Grandes chances desperdiçadas: {statistics['bigChancesMissed']}\n"
        f"Passes precisos: {statistics['accuratePasses']}\n"
        f"Passes imprecisos: {statistics['inaccuratePasses']}\n"
        f"Total de passes: {statistics['totalPasses']}\n"
        f"Passes chaves: {statistics['keyPasses']}\n"
        f"Dribles bem sucedidos: {statistics['successfulDribbles']}\n"
        f"Cortes: {statistics['tackles']}\n"
        f"Intercepções: {statistics['interceptions']}\n"
        f"Cartões amarelos: {statistics['yellowCards']}\n"
        f"Cartões vermelhos: {statistics['redCards']}\n"
        f"Cruzamentos precisos: {statistics['accurateCrosses']}\n"
        f"Total de chutes: {statistics['totalShots']}\n"
        f"Chutes no alvo: {statistics['shotsOnTarget']}\n"
        f"Chutes fora do alvo: {statistics['shotsOffTarget']}\n"
        f"Duelos ganhos no chão: {statistics['groundDuelsWon']}\n"
        f"Duelos aereos ganhos: {statistics['aerialDuelsWon']}\n"
        f"Total de duelos ganhos: {statistics['totalDuelsWon']}\n"
        f"Minutos jogados: {statistics['minutesPlayed']}\n"
        f"Penalidades sofridas: {statistics['penaltiesTaken']}\n"
        f"Gols de penalti: {statistics['penaltyGoals']}\n"
        f"Penaltis concedidos: {statistics['penaltyConceded']}\n"
        f"Gols de falta: {statistics['freeKickGoal']}\n"
        f"Gols na pequena área: {statistics['goalsFromInsideTheBox']}\n"
        f"Gols de fora da pequena área: {statistics['goalsFromOutsideTheBox']}\n"
        f"Chutes de dentro da pequena área: {statistics['shotsFromInsideTheBox']}\n"
        f"Chutes de fora da pequena área: {statistics['shotsFromOutsideTheBox']}\n"
        f"Gols de cabeça: {statistics['headedGoals']}\n"
        f"Gols de pé esquerdo: {statistics['leftFootGoals']}\n"
        f"Gols de pé direito: {statistics['rightFootGoals']}\n"
        f"Bolas longas precisas: {statistics['accurateLongBalls']}\n"
        f"Perda de posse: {statistics['possessionLost']}\n"
        f"Toques na bola: {statistics['touches']}\n"
        f"Derrubado: {statistics['wasFouled']}\n"
        f"Faltas: {statistics['fouls']}\n"
        f"Gols contra: {statistics['ownGoals']}\n"
        f"Impedimento: {statistics['offsides']}\n"
        f"Chutes bloqueados: {statistics['blockedShots']}\n"
        f"Passes para assistencia: {statistics['passToAssist']}\n"
        f"Penaltis convertidos: {statistics['penaltyConversion']}\n"
        f"Total de tentativas de assistencia: {statistics['totalAttemptAssist']}\n"
        f"Total de disputas: {statistics['totalContest']}\n"
        f"Total de cruzamentos: {statistics['totalCross']}\n"
        f"Duelos perdidos: {statistics['duelLost']}\n"
        f"Perdas áereas: {statistics['aerialLost']}\n"
        f"Tentativas de penalti perdidas: {statistics['attemptPenaltyMiss']}\n"
        # f"Assistencias: {statistics['assists']}\n"
    )
    bot.answer_callback_query(
        callback_query_id=call.id, text='Carregando estatisticas'
    )
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id
    )
    sleep(0.7)
    bot.send_message(call.message.chat.id, overall_message)


@bot.message_handler(commands=['help', 'ajuda'])
def help_command(message):
    """Send the bot User Guide to the user."""
    CHAT_ID = message.chat.id
    string = (
        f'Lista de comandos disponiveis: \n'
        f'\n/ultimos_resultados_bra : ultimos resultados do brasileirão A.\n'
        f'\n/tabela_bra : tabela do brasileirão A.\n'
        f'\n/resumo_time_bra : Overview e estatisticas de qualquer clube do'
        f' brasileirão\n'
        f'\n/confrontos_por_rodada_bra : Confrontos que aconteceram ou irão'
        f' acontecer\n'
        f'\n/jogador_por_time_bra : Overall do jogador\n'
    )
    bot.send_message(CHAT_ID, string)


@bot.message_handler(commands=['start'])
def start_message(message):
    """Shows the user guide message and the keyboard buttons."""
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    keyboard.row('/ultimos_resultados_bra')
    keyboard.row('/tabela_bra')
    keyboard.row('/resumo_time_bra')
    keyboard.row('/confrontos_por_rodada_bra')
    keyboard.row('/jogador_por_tima_bra')
    user_guide_message = (
        f'Bem vindo ao Fute Bot ⚽️ ! \n'
        f'Escreva ou aperte um dos botões que aparecem no seu teclado. '
        f"Caso tenha alguma dificuldade, digite ou aperte '/help' '/ajuda' "
        f'para ver a lista de comandos disponiveis. '
        f"Os comandos com o sufixo 'BRA' correspondem ao brasileirão série A."
    )
    bot.send_message(
        message.chat.id, user_guide_message, reply_markup=keyboard
    )


bot.polling()
