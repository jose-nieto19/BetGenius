#!/bin/python

import requests
import json
import time
from datetime import datetime
import telebot

msg_partidos=""
msg_predicciones=""

uri = f'https://api.football-data.org/v4/matches'
headers = { 'X-Auth-Token': 'XXXXXXXXXXXXXXXXXXXXXX', 'Accept-Encoding': ''}

response = requests.get(uri, headers=headers)
json_response=response.json()

#MOSTRAR LOS PARTIDOS DEL DIA
date = datetime.now()
day=date.day
if(day<10):
    day="0"+str(day)
month=date.month
if(month<10):
    month="0"+str(month)
year=date.year

msg_partidos=msg_partidos+"***********PARTIDOS DEL DIA: "+str(day)+"/"+str(month)+"/"+str(year)+" ************\n\n"
msg_predicciones=msg_predicciones+"***********PREDICCIONES DEL DIA: "+str(day)+"/"+str(month)+"/"+str(year)+" ************\n\n"
count_matches=0

for match in json_response["matches"]:
    date = str(int(match["utcDate"][11:13]) + 2)+":"+match["utcDate"][14:16]
    msg_partidos=msg_partidos+"COMPETICIÓN: "+match["competition"]["name"]+"\nPARTIDO: "+match["homeTeam"]["name"]+"- "+match["awayTeam"]["name"]+"\nHORA INICIO: " + date + "h\n-------------------------------------------\n"

for match in json_response["matches"]:
    
    count_matches=count_matches+1
    if count_matches<=3:
    
        id_match=match["id"]
        competition_type=match["competition"]["type"]
        competition_code=match["competition"]["code"]
        equipo_local=match["homeTeam"]["name"]
        equipo_visitante=match["awayTeam"]["name"]
    
        #PROBABILIDAD TENIENDO EN CUENTA LOS ULTIMOS 15 ENFRENTAMIENTOS ENTRE AMBOS EQUIPOS
        uri_enfrentamientos=f'https://api.football-data.org/v4/matches/{id_match}/head2head?limit=15'
        response = requests.get(uri_enfrentamientos, headers=headers)
        json_enfrentamientos=response.json()
        record=json_enfrentamientos["aggregates"]
        num_matches=record["numberOfMatches"]
        wins_homeTeam=record["homeTeam"]["wins"]
        pb_win_hTeam=wins_homeTeam/num_matches
        draws=record["homeTeam"]["draws"]
        pb_draw=draws/num_matches
        wins_awayTeam=record["homeTeam"]["losses"]
        pb_win_aTeam=wins_awayTeam/num_matches
    
        if competition_type=="CUP":  
            more_probability=max(pb_win_aTeam,pb_win_hTeam,pb_draw)
            if more_probability==pb_win_hTeam:
                msg_predicciones=msg_predicciones+"\nPARTIDO: "+equipo_local+ " - "+equipo_visitante+"\nPREDICCION: "+equipo_local+" GANA EL PARTIDO\n-------------------------------------------\n"
            elif more_probability==pb_draw:
                msg_predicciones=msg_predicciones+"\nPARTIDO: "+equipo_local+ " - "+equipo_visitante+"\nPREDICCION: EMPATE\n-------------------------------------------\n"
            else:
                msg_predicciones=msg_predicciones+"\nPARTIDO: "+equipo_local+ " - "+equipo_visitante+"\nPREDICCION: "+equipo_visitante+" GANA EL PARTIDO\n-------------------------------------------\n"

        elif competition_type=="LEAGUE": #PROBABILIDAD ANTERIOR COMBINANDOLA CON LA CALCULADA TENIENDO EN CUENTA LA CLASIFICACION DE LA LIGA
        
            uri_table=f'https://api.football-data.org/v4/competitions/{competition_code}/standings'
            response_table = requests.get(uri_table, headers=headers)
            json_table=response_table.json()
            
            clasificacion_global=json_table["standings"][0]["table"]
            clasificacion_local=json_table["standings"][1]["table"]
            clasificacion_visitante=json_table["standings"][2]["table"]

            for equipo in clasificacion_local:
                if equipo["team"]["name"]==equipo_local:
                    partidos_jugados_local=equipo["playedGames"]
                    ganados_local=equipo["won"]
                    probabilidad_win_local=ganados_local/partidos_jugados_local
                    empatados_local=equipo["draw"]
                    probabilidad_draw_local=empatados_local/partidos_jugados_local
                    perdidos_local=equipo["lost"]
                    probabilidad_lost_local=perdidos_local/partidos_jugados_local
            for equipo in clasificacion_visitante:
                if equipo["team"]["name"]==equipo_visitante:
                    partidos_jugados_visitante=equipo["playedGames"]
                    ganados_visitante=equipo["won"]
                    probabilidad_win_visitante=ganados_visitante/partidos_jugados_visitante
                    empatados_visitante=equipo["draw"]
                    probabilidad_draw_visitante=empatados_visitante/partidos_jugados_visitante
                    perdidos_visitante=equipo["lost"]
                    probabilidad_lost_visitante=perdidos_visitante/partidos_jugados_visitante
    
            #Definir las probabilidades previas de cada suceso teniendo en cuenta solo la clasificación
            prob_victoria_local = (ganados_local+perdidos_visitante)/(partidos_jugados_local+partidos_jugados_visitante)
            prob_empate = (empatados_local+empatados_visitante)/(partidos_jugados_local+partidos_jugados_visitante)
            prob_victoria_visitante = (perdidos_local+ganados_visitante)/(partidos_jugados_local+partidos_jugados_visitante)

            #Calculo de la probabilidad total
            pb2_win_local=(pb_win_hTeam+prob_victoria_local)/2
            pb2_draw=(pb_draw+prob_empate)/2
            pb2_win_visitante=(pb_win_aTeam+prob_victoria_visitante)/2
            pb2_suma=pb2_win_local+pb2_draw+pb2_win_visitante
            pb_total_win_local=pb2_win_local/pb2_suma
            pb_total_draw=pb2_draw/pb2_suma
            pb_total_win_visitante=pb2_win_visitante/pb2_suma
            more_probability=max(pb_total_win_local,pb_total_draw,pb_total_win_visitante)
    
            if more_probability==pb_total_win_local:
                msg_predicciones=msg_predicciones+"\nPARTIDO: "+equipo_local+ " - "+equipo_visitante+"\nPREDICCION: "+equipo_local+" GANA EL PARTIDO\n-------------------------------------------\n"
            elif more_probability==pb_total_draw:
                msg_predicciones=msg_predicciones+"\nPARTIDO: "+equipo_local+ " - "+equipo_visitante+"\nPREDICCION: EMPATE\n-------------------------------------------\n"
            else:
                msg_predicciones=msg_predicciones+"\nPARTIDO: "+equipo_local+ " - "+equipo_visitante+"\nPREDICCION: "+equipo_visitante+" GANA EL PARTIDO\n-------------------------------------------\n"


bot = telebot.TeleBot("XXXXXXXXXXXXXXXXXXXXXX", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
#bot.set_webhook()

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Hola! Bienvenid@ al bot de BetGenius. Elige con los botones del teclado si quieres que te envíe los partidos que hay en el día de hoy o las predicciones para ellos.")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Hola! Bienvenid@ al bot de BetGenius. Esto es lo que hace cada comando:\n /partidos - Te envío los horarios de los partidos que hay en el día de hoy.\n /predicciones - Te envío las predicciones para los partidos que hay en el día de hoy.\n /start - Te envío un mensaje de bienvenida al bot.\n /help - Solicitas ayuda para saber que hace cada comando y te envío la información de ello.")
	
@bot.message_handler(commands=['partidos'])
def send_partidos(message):
	bot.reply_to(message, msg_partidos)
	
@bot.message_handler(commands=['predicciones'])
def send_predicciones(message):
	bot.reply_to(message, msg_predicciones)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, "Este mensaje o comando no vale. Utiliza los botones del teclado.")
	
uri = f'https://api.football-data.org/v4/matches'
headers = { 'X-Auth-Token': 'XXXXXXXXXXXXXXXXXXXXXX', 'Accept-Encoding': ''}
response = requests.get(uri, headers=headers)
if (response.status_code == 200):
    print("API Football --> OK")

if (bot.get_me() is not None):
    print("Bot Telegram --> OK")
	
bot.infinity_polling()
